
import argparse
from cProfile import run
import os
import re
import time
import json

import torch

from math import ceil
#from scienceworld import ScienceWorldEnv
from scienceworld import BufferedHistorySaver
from transformers import T5Tokenizer, T5ForConditionalGeneration
from textworld_express import TextWorldExpressEnv
from symbolicModule import *


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Original functions
# def build_input_str_behavior_cloning(task_description, prev_obs, prev_action, cur_obs, cur_look, cur_inv):
#     outStr = task_description + ' </s> ' + cur_obs + ' ' + cur_inv + ' ' + cur_look + ' </s> <extra_id_0>' + ' </s> ' + prev_action + ' </s> ' + prev_obs + ' </s>'
#     outStr = sanitizeStr(outStr)
#     return outStr

# def build_input_str_decision_transformer(task_description, prev_obs, prev_action, cur_obs, cur_look, cur_inv, cur_score):
#     returns_to_go = 1.0 - float(cur_score)
#     returns_to_go = round(returns_to_go, 2)
#     outStr = task_description + ' </s>' + str(returns_to_go) + '</s> '+  cur_obs + ' ' + cur_inv + ' ' + cur_look + ' </s> <extra_id_0>' + ' </s> ' + prev_action + ' </s> ' + prev_obs + ' </s>'

#     outStr = sanitizeStr(outStr)
#     return outStr

# Peter's changes that include cue tokens at the start of each element
def build_input_str_behavior_cloning(task_description, prev_obs, prev_action, cur_obs, cur_look, cur_inv):
    outStr = task_description + ' </s> OBS ' + cur_obs + ' </s> INV ' + cur_inv + ' </s> LOOK ' + cur_look + ' </s> <extra_id_0>' + ' </s> PACT ' + prev_action + ' </s> POBS ' + prev_obs + ' </s>'
    outStr = sanitizeStr(outStr)
    return outStr

def build_input_str_decision_transformer(task_description, prev_obs, prev_action, cur_obs, cur_look, cur_inv, cur_score):
    returns_to_go = 1.0 - float(cur_score)
    returns_to_go = round(returns_to_go, 2)
    outStr = task_description + ' </s> RET ' + str(returns_to_go) + '</s> OBS '+  cur_obs + ' </s> INV ' + cur_inv + ' </s> LOOK ' + cur_look + ' </s> <extra_id_0>' + ' </s> PACT ' + prev_action + ' </s> POBS ' + prev_obs + ' </s>'

    outStr = sanitizeStr(outStr)
    return outStr


def sanitizeStr(inStr):
    out = inStr.replace("\n", " ")
    out = out.replace("\t", " ")
    return out

def post_process_generation(raw_pred):
    ans_match = re.match(r".*<extra_id_0>(.*)<extra_id_1>.*", raw_pred)
    if ans_match is not None:
        result = ans_match.group(1)
    else:
        result = raw_pred

    # remove extra <*>'s left in
    result = result.replace("<", " <")
    out = ""
    for token in result.split(" "):
        if (len(token.strip()) > 0):
            if (token[0] != "<"):
                out += token + " "
    result = out

    return result.strip()

#
#   Valid action alignment
#
def findValidAction(predictions, validActions, lastActions):

    # Go down the ranked list of LM-generated actions.  If one of them is on the valid action list, choose it.
    for pred in predictions:
        if (pred.strip() in validActions):
            #if (pred not in lastActions):      # This was in the old agent -- trying to prevent it from repeating actions.  Disable here.
            return pred

    # If not, then try to find the cosine of the best action
    tokensPred = predictions[0].split(" ")
    uniqueTokensPred = set(tokensPred)

    topAction = predictions[0]
    topValue = 0
    for validAction in validActions:
        if (validAction not in lastActions):
            tokensAction = validAction.split(" ")
            uniqueTokensAction = set(tokensAction)

            intersection = uniqueTokensPred.intersection(uniqueTokensAction)
            if (len(intersection) > topValue):
                topAction = validAction
                topValue = len(intersection)

    # Sanitize top action
    topAction = re.sub(r'[^A-Za-z0-9 ]+', '', topAction)
    return topAction



#
#   TextWorldExpress Initialization
#

# Initialize a TextWorldExpress environment directly from the API
def initializeEnv(threadNum, args):
    gameName = args["game_name"]
    gameParams = args["game_params"]

    env = TextWorldExpressEnv(args["jar_path"], envStepLimit=args["max_steps"])
    #env.load(gameName, gameFold="train", seed=0, paramStr=gameParams, generateGoldPath=False)
    env.load(gameName, gameParams)

    return env

#
# Reset the environment (with a new randomly selected variation)
#
def resetWithVariation(env, args, gameFold, seed, generateGoldPath=False):
    gameName = args["game_name"]
    gameParams = args["game_params"]

    env.load(gameName, gameParams)
    _, info = env.reset(seed, gameFold, generateGoldPath=generateGoldPath)    # New TWX API

    enabledModules = args["useSymbolicModules"].split(",")

    properties = env.getGenerationProperties()
    moduleInterface = SymbolicModuleInterface(enabledModules, properties)


    return info, moduleInterface

def resetWithVariationTrain(env, args, seed, generateGoldPath=False):
    return resetWithVariation(env, args, "train", seed, generateGoldPath)

def resetWithVariationDev(env, args, seed, generateGoldPath=False):
    return resetWithVariation(env, args, "dev", seed, generateGoldPath)

def resetWithVariationTest(env, args, seed, generateGoldPath=False):
    return resetWithVariation(env, args, "test", seed, generateGoldPath)

#
#   Sanitization
#
#
#   Input/Output sanitization
#
def sanitizeInfo(infoIn, moduleInterface):
    # Convert from py4j.java_collections.JavaList to python list

    #print("SanitizeInfo:" + str(infoIn)
    ## PJ: Added 02/17/2023, for API meshing.
    # If no 'lastActionStr', then this is the first observation.  Set it to the empty string.
    if ('lastActionStr' not in infoIn):
        infoIn['lastActionStr'] = ""

    # Recast the list from the py4j interface
    validActions = []
    for elem in infoIn['validActions']:
        validActions.append(elem)

    # Add any valid actions from the module
    validActions.extend(moduleInterface.getValidCommands())

    # Bug: Reward is currently missing from TextWorldExpress in the first observation.
    reward = 0
    if ('reward' in infoIn):
        reward = infoIn['reward']

    # Set isDone = True if either success or failure conditions are set.
    isDone = False
    if ((infoIn['tasksuccess'] == True) or (infoIn['taskfailure'] == True)):
        isDone = True

    # Keep track of the last module command sent, if one was
    moduleCommand = ""
    if ('moduleCommand' in infoIn):
        moduleCommand = infoIn['moduleCommand']

    # TextWorldExpress
    info = {'obs': infoIn['observation'],
            'moves': 0, # Not currently supported
            'reward': reward,
            'score': infoIn['score'],
            'look': infoIn['look'],
            'inv': infoIn['inventory'],
            'valid': validActions,
            'done': isDone,
            'taskDescription': infoIn['taskDescription'],
            'taskDesc': infoIn['taskDescription'],              # Two different keys this information sometimes appears as
            'lastActionStr': infoIn['lastActionStr'],
            'moduleCommand': moduleCommand
        }


    return info

# Append the result of the module as an observation
def addModuleResultToInfo(infoIn, moduleResult, moduleCommand):
    infoIn['obs'] = moduleResult
    infoIn['observation'] = moduleResult
    infoIn['moduleCommand'] = moduleCommand
    return infoIn



#
#   Generating training data for the T5 agent
#

# Run gold paths from the training set, and save their histories (that we can use for generating training data)
# This is specific to the 'Artihmetic' game
def runGoldPathsArithmetic(args):
    # Initialize the environment
    env = initializeEnv(threadNum=2, args=args)

    # Pick which set to build gold paths from
    variations = []
    if (args["set"] == "train"):
        variations = list(env.getValidSeedsTrain())
    elif (args["set"] == "dev"):
        variations = list(env.getValidSeedsDev())
    elif (args["set"] == "test"):
        variations = list(env.getValidSeedsTest())
    else:
        print("ERROR: Unknown set to build path training data from (" + str(args["set"]) + ")")
        exit(1)

    # Determine a (sub)set of variations to run
    maxVariations = args['num_variations']
    if (len(variations) > maxVariations):
        print("NOTE: More than " + str(maxVariations) + " variations.  Only evaluating 100.")
        variations = variations[:maxVariations]

    # A record of all the histories, that we'll use to generate the training data strings later
    histories = []

    # Keep track of the number of errors, if any
    errors = []

    # Run each variation in the training set
    for variationIdx in variations:
        print("Resetting with variation " + str(variationIdx))


        info = None
        moduleInterface = None
        # Reset with this new variation(seed), based on the set
        if (args["set"] == "train"):
            info, moduleInterface = resetWithVariationTrain(env, args, variationIdx, generateGoldPath=True)
        elif (args["set"] == "dev"):
            info, moduleInterface = resetWithVariationDev(env, args, variationIdx, generateGoldPath=True)
        elif (args["set"] == "test"):
            info, moduleInterface = resetWithVariationTest(env, args, variationIdx, generateGoldPath=True)
        else:
            print("ERROR: Unrecognized set to evaluate on (" + str(args["set"]) + ")")
            exit(1)
        info = sanitizeInfo(info, moduleInterface)

        # Get gold path
        goldPath = env.getGoldActionSequence()
        print("Gold action sequence: " + str(goldPath))

        # TODO: Add in a calculator gold action
        if ((args["game_name"] == "arithmetic") and ("calc" in moduleInterface.getEnabledModuleNames())):
            genProps = env.getGenerationProperties()
            num1 = genProps['hidden_num1']
            num2 = genProps['hidden_num2']
            calcOp = genProps['hidden_op']
            calcAction = ""
            if (calcOp == 0):
                calcOp = 'add'
                calcAction = calcOp + " " + str(num1) + " " + str(num2)
            elif (calcOp == 1):
                calcOp = 'sub'
                calcAction = calcOp + " " + str(num1) + " " + str(num2)
            elif (calcOp == 2):
                calcOp = 'mul'
                calcAction = calcOp + " " + str(num1) + " " + str(num2)
            elif (calcOp == 3):
                calcOp = 'div'
                calcAction = calcOp + " " + str(num1) + " " + str(num2)
            else:
                print("ERROR: Unrecognized calcOp (" + str(calcOp) + ")")
                exit(1)

            # Insert the action to the gold path
            goldPath.insert(3, calcAction)

            print("New gold action sequence: " + str(goldPath))



        task_description = ""   # TODO: Currently no task description
        lastRawInfo = info
        score = 0.0
        step = 0

        history = []

        # Save initial observation
        info['stepsSinceLastReset'] = step
        history.append(info.copy())

        # Run each action in the gold path
        for actionToTake in goldPath:
            print("Next gold action: " + actionToTake)

            # Take a step in the environment
            # First, check to see if the command is intended for a module
            moduleWasRun, moduleResult = moduleInterface.runCommand(actionToTake)
            if (moduleWasRun == True):
                # Symbolic module was run -- add result to current 'info'
                #print("Info (before): ")
                #print(info)
                info = addModuleResultToInfo(lastRawInfo, moduleResult, actionToTake)
                lastRawInfo['lastActionStr'] = ""
                #print("Info (after): ")
                #print(info)

            else:
                # Command was not intended for symbolic module -- run environment
                _, _, _, info = env.step(actionToTake)
                lastRawInfo = info

            # TODO: Give observations to moduleInterface

            info = sanitizeInfo(info, moduleInterface)
            obs = info['obs']
            reward = info['reward']
            done = info['done']
            score = info['score']

            # Save history
            info['stepsSinceLastReset'] = step
            history.append(info.copy())

            print("Obs: " + obs)
            print(f"Variation: {variationIdx}, Step: {step}, Score: {score}, Action: {actionToTake}")
            print("")
            step += 1


        # Store history
        # Get history internally (keeps track of module commands)
        finalScore = 0
        if (len(history) > 0):
            finalScore = history[-1]['score']

        runHistory = {
            'finalScore': finalScore,
            'history': history,
        }

        histories.append(runHistory)

        # TODO: Check that score is 1.0
        if (score < 1.0):
            warningStr = "WARNING: Score for this variation (" + str(variationIdx) + ") is less than 1.0.  This may be an error in the gold path."
            print(warningStr)
            errors.append(warningStr)

        print("Run completed...")

    # If there were any warnings/errors, print these out at the end so they're easily visible to the user
    if (len(errors) > 0):
        print ("Warnings/Errors: " + str(errors))
        print ("\n".join(errors))

    # Return the histories/trajectories from running the gold paths:
    return histories


# Run gold paths from the training set, and save their histories (that we can use for generating training data)
# This is specific to the 'MapReader' game
def runGoldPathsMapReader(args):
    # Initialize the environment
    env = initializeEnv(threadNum=2, args=args)

    # Pick which set to build gold paths from
    variations = []
    if (args["set"] == "train"):
        variations = list(env.getValidSeedsTrain())
    elif (args["set"] == "dev"):
        variations = list(env.getValidSeedsDev())
    elif (args["set"] == "test"):
        variations = list(env.getValidSeedsTest())
    else:
        print("ERROR: Unknown set to build path training data from (" + str(args["set"]) + ")")
        exit(1)

    # Determine a (sub)set of variations to run
    maxVariations = args['num_variations']
    if (len(variations) > maxVariations):
        print("NOTE: More than " + str(maxVariations) + " variations.  Only evaluating 100.")
        variations = variations[:maxVariations]

    # A record of all the histories, that we'll use to generate the training data strings later
    histories = []

    # Keep track of the number of errors, if any
    errors = []

    # Run each variation in the training set
    for variationIdx in variations:
        print("Resetting with variation " + str(variationIdx))


        info = None
        moduleInterface = None
        # Reset with this new variation(seed), based on the set
        if (args["set"] == "train"):
            info, moduleInterface = resetWithVariationTrain(env, args, variationIdx, generateGoldPath=True)
        elif (args["set"] == "dev"):
            info, moduleInterface = resetWithVariationDev(env, args, variationIdx, generateGoldPath=True)
        elif (args["set"] == "test"):
            info, moduleInterface = resetWithVariationTest(env, args, variationIdx, generateGoldPath=True)
        else:
            print("ERROR: Unrecognized set to evaluate on (" + str(args["set"]) + ")")
            exit(1)
        lastRawInfo = info.copy()
        # Give modules initial observations
        moduleInterface.giveEnvironmentStatus(lastRawInfo['observation'], lastRawInfo['inventory'], lastRawInfo['look'])

        # Sanitize info, and add in module commands to valid actions
        info = sanitizeInfo(info, moduleInterface)


        # Get gold path
        goldPath = env.getGoldActionSequence()
        print("Gold action sequence: " + str(goldPath))

        # Get task description
        taskDescription = env.getTaskDescription()
        # Extract out the target location from the task description
        coinLocation = re.search('located in the (.*)', taskDescription).group(1).split(",")[0].strip()
        firstObsSent = info["look"].split(".")[0]
        startLocation = firstObsSent.strip().split("You are in the ")[1]

        print("Coin location: " + coinLocation)
        print("Start Location: " + startLocation)

        # TODO: Add in a map reading gold action(s)
        if ((args["game_name"].startswith("mapreader")) and ("navigation" in moduleInterface.getEnabledModuleNames())):

            # Find the index of the map reading action
            mapReadingActionIdx = goldPath.index("read map")

            # Insert actions that ask for navigation information (to the task location)
            idx = mapReadingActionIdx + 1
            while (idx < len(goldPath)):
                curAction = goldPath[idx]
                # If the gold action is picking up the coin, then stop.
                if (curAction == "take coin"):
                    break

                # If the gold action is not picking up the coin, then it's navigation -- add a navigation module command
                goldPath.insert(idx, "next step to " + coinLocation)
                idx += 2


            # Find the index of the 'take coin' action
            mapReadingActionIdx = goldPath.index("take coin")

            # Insert actions that ask for navigation information (back to the start location)
            idx = mapReadingActionIdx + 1
            while (idx < len(goldPath)):
                curAction = goldPath[idx]
                # If the gold action is picking up the coin, then stop.
                if (curAction == "put coin in box"):
                    break

                # If the gold action is not picking up the coin, then it's navigation -- add a navigation module command
                goldPath.insert(idx, "next step to " + startLocation)
                idx += 2

            print("New gold action sequence: " + str(goldPath))



        #task_description = ""   # TODO: Currently no task description
        score = 0.0
        step = 0

        history = []

        # Save initial observation
        info['stepsSinceLastReset'] = step
        history.append(info.copy())

        # Run each action in the gold path
        for actionToTake in goldPath:
            print("Next gold action: " + actionToTake)

            # Take a step in the environment
            # First, check to see if the command is intended for a module
            moduleWasRun, moduleResult = moduleInterface.runCommand(actionToTake)
            if (moduleWasRun == True):
                # Symbolic module was run -- add result to current 'info'
                #print("Info (before): ")
                #print(info)
                info = addModuleResultToInfo(lastRawInfo, moduleResult, actionToTake)
                lastRawInfo['lastActionStr'] = ""
                #print("Info (after): ")
                #print(info)

            else:
                # Command was not intended for symbolic module -- run environment
                _, _, _, info = env.step(actionToTake)
                lastRawInfo = info

            # Give modules new observations
            moduleInterface.giveEnvironmentStatus(lastRawInfo['observation'], lastRawInfo['inventory'], lastRawInfo['look'])

            # Sanitize info, and add in module commands to valid actions
            info = sanitizeInfo(info, moduleInterface)
            obs = info['obs']
            reward = info['reward']
            done = info['done']
            score = info['score']

            # Save history
            info['stepsSinceLastReset'] = step
            history.append(info.copy())

            print("Obs: " + obs)
            print(f"Variation: {variationIdx}, Step: {step}, Score: {score}, Action: {actionToTake}")
            print("")
            step += 1


        # Store history
        # Get history internally (keeps track of module commands)
        finalScore = 0
        if (len(history) > 0):
            finalScore = history[-1]['score']

        runHistory = {
            'finalScore': finalScore,
            'history': history,
        }

        histories.append(runHistory)

        # TODO: Check that score is 1.0
        if (score < 1.0):
            warningStr = "WARNING: Score for this variation (" + str(variationIdx) + ") is less than 1.0.  This may be an error in the gold path."
            print(warningStr)
            errors.append(warningStr)

        print("Run completed...")

    # If there were any warnings/errors, print these out at the end so they're easily visible to the user
    if (len(errors) > 0):
        print ("Warnings/Errors: " + str(errors))
        print ("\n".join(errors))

    # Return the histories/trajectories from running the gold paths:
    return histories



# Run gold paths from the training set, and save their histories (that we can use for generating training data)
# This is specific to the 'Sorting' game
def runGoldPathsSorting(args):
    # Initialize the environment
    env = initializeEnv(threadNum=2, args=args)

    # Pick which set to build gold paths from
    variations = []
    if (args["set"] == "train"):
        variations = list(env.getValidSeedsTrain())
    elif (args["set"] == "dev"):
        variations = list(env.getValidSeedsDev())
    elif (args["set"] == "test"):
        variations = list(env.getValidSeedsTest())
    else:
        print("ERROR: Unknown set to build path training data from (" + str(args["set"]) + ")")
        exit(1)

    # Determine a (sub)set of variations to run
    maxVariations = args['num_variations']
    if (len(variations) > maxVariations):
        print("NOTE: More than " + str(maxVariations) + " variations.  Only evaluating 100.")
        variations = variations[:maxVariations]

    # A record of all the histories, that we'll use to generate the training data strings later
    histories = []

    # Keep track of the number of errors, if any
    errors = []

    # Run each variation in the training set
    for variationIdx in variations:
        print("Resetting with variation " + str(variationIdx))


        info = None
        moduleInterface = None
        # Reset with this new variation(seed), based on the set
        if (args["set"] == "train"):
            info, moduleInterface = resetWithVariationTrain(env, args, variationIdx, generateGoldPath=True)
        elif (args["set"] == "dev"):
            info, moduleInterface = resetWithVariationDev(env, args, variationIdx, generateGoldPath=True)
        elif (args["set"] == "test"):
            info, moduleInterface = resetWithVariationTest(env, args, variationIdx, generateGoldPath=True)
        else:
            print("ERROR: Unrecognized set to evaluate on (" + str(args["set"]) + ")")
            exit(1)
        lastRawInfo = info.copy()

        # Give modules initial observations
        moduleInterface.giveEnvironmentStatus(lastRawInfo['observation'], lastRawInfo['inventory'], lastRawInfo['look'])

        # Sanitize info, and add in module commands to valid actions
        info = sanitizeInfo(info, moduleInterface)


        # Get gold path
        goldPath = env.getGoldActionSequence()
        print("Gold action sequence: " + str(goldPath))

        # Get task description
        taskDescription = env.getTaskDescription()

        # Add in calls to sorting module to gold action sequence
        if ((args["game_name"] == "sorting") and ("sortquantity" in moduleInterface.getEnabledModuleNames())):

            # Essentially here, we're just inserting a 'sort ascending' module call before each 'take/put' pick-and-place action sequence.
            goldPathOut = []
            for action in goldPath:
                if (action.lower().startswith("take")):
                    # Insert 'sort' actio before take
                    goldPathOut.append("sort ascending")
                    goldPathOut.append(action)
                else:
                    goldPathOut.append(action)

            goldPath = goldPathOut

            print("New gold action sequence: " + str(goldPath))



        #task_description = ""   # TODO: Currently no task description
        score = 0.0
        step = 0

        history = []

        # Save initial observation
        info['stepsSinceLastReset'] = step
        history.append(info.copy())

        # Run each action in the gold path
        for actionToTake in goldPath:
            print("Next gold action: " + actionToTake)

            # Take a step in the environment
            # First, check to see if the command is intended for a module
            moduleWasRun, moduleResult = moduleInterface.runCommand(actionToTake)
            if (moduleWasRun == True):
                # Symbolic module was run -- add result to current 'info'
                #print("Info (before): ")
                #print(info)
                info = addModuleResultToInfo(lastRawInfo, moduleResult, actionToTake)
                lastRawInfo['lastActionStr'] = ""
                #print("Info (after): ")
                #print(info)

            else:
                # Command was not intended for symbolic module -- run environment
                _, _, _, info = env.step(actionToTake)
                lastRawInfo = info.copy()

            # Give modules new observations
            moduleInterface.giveEnvironmentStatus(lastRawInfo['observation'], lastRawInfo['inventory'], lastRawInfo['look'])

            # Sanitize info, and add in module commands to valid actions
            info = sanitizeInfo(info, moduleInterface)
            obs = info['obs']
            reward = info['reward']
            done = info['done']
            score = info['score']

            # Save history
            info['stepsSinceLastReset'] = step
            history.append(info.copy())

            print("Obs: " + obs)
            print(f"Variation: {variationIdx}, Step: {step}, Score: {score}, Action: {actionToTake}")
            print("")
            step += 1


        # Store history
        # Get history internally (keeps track of module commands)
        finalScore = 0
        if (len(history) > 0):
            finalScore = history[-1]['score']

        runHistory = {
            'finalScore': finalScore,
            'history': history,
        }

        histories.append(runHistory)

        # TODO: Check that score is 1.0
        if (score < 1.0):
            warningStr = "WARNING: Score for this variation (" + str(variationIdx) + ") is less than 1.0.  This may be an error in the gold path."
            print(warningStr)
            errors.append(warningStr)

        print("Run completed...")

    # If there were any warnings/errors, print these out at the end so they're easily visible to the user
    if (len(errors) > 0):
        print ("Warnings/Errors: " + str(errors))
        print ("\n".join(errors))

    # Return the histories/trajectories from running the gold paths:
    return histories


# Run gold paths from the training set, and save their histories (that we can use for generating training data)
# This is specific to the 'TWC' game
def runGoldPathsTWC(args):
    # Initialize the environment
    env = initializeEnv(threadNum=2, args=args)

    # Pick which set to build gold paths from
    variations = []
    if (args["set"] == "train"):
        variations = list(env.getValidSeedsTrain())
    elif (args["set"] == "dev"):
        variations = list(env.getValidSeedsDev())
    elif (args["set"] == "test"):
        variations = list(env.getValidSeedsTest())
    else:
        print("ERROR: Unknown set to build path training data from (" + str(args["set"]) + ")")
        exit(1)

    # Determine a (sub)set of variations to run
    maxVariations = args['num_variations']
    if (len(variations) > maxVariations):
        print("NOTE: More than " + str(maxVariations) + " variations.  Only evaluating 100.")
        variations = variations[:maxVariations]

    # A record of all the histories, that we'll use to generate the training data strings later
    histories = []

    # Keep track of the number of errors, if any
    errors = []

    # Run each variation in the training set
    for variationIdx in variations:
        print("Resetting with variation " + str(variationIdx))


        info = None
        moduleInterface = None
        # Reset with this new variation(seed), based on the set
        if (args["set"] == "train"):
            info, moduleInterface = resetWithVariationTrain(env, args, variationIdx, generateGoldPath=True)
        elif (args["set"] == "dev"):
            info, moduleInterface = resetWithVariationDev(env, args, variationIdx, generateGoldPath=True)
        elif (args["set"] == "test"):
            info, moduleInterface = resetWithVariationTest(env, args, variationIdx, generateGoldPath=True)
        else:
            print("ERROR: Unrecognized set to evaluate on (" + str(args["set"]) + ")")
            exit(1)
        lastRawInfo = info.copy()

        # Give modules initial observations
        moduleInterface.giveEnvironmentStatus(lastRawInfo['observation'], lastRawInfo['inventory'], lastRawInfo['look'])

        # Sanitize info, and add in module commands to valid actions
        info = sanitizeInfo(info, moduleInterface)


        # Get gold path
        goldPath = env.getGoldActionSequence()
        print("Gold action sequence: " + str(goldPath))

        # Get task description
        taskDescription = env.getTaskDescription()

        # Add in KB lookup actions to gold path
        if ((args["game_name"] == "twc") and ("kb-twc" in moduleInterface.getEnabledModuleNames())):

            # Essentially here, we're just inserting a 'sort ascending' module call before each 'take/put' pick-and-place action sequence.
            goldPathOut = []
            for action in goldPath:
                goldPathOut.append(action)
                if (action.lower().startswith("take")):
                    # Insert a KB lookup for the item location after the 'take'
                    itemName = action[len("take "):].strip()
                    goldPathOut.append("query " + itemName)

            goldPath = goldPathOut

            print("New gold action sequence: " + str(goldPath))


        #task_description = ""   # TODO: Currently no task description
        score = 0.0
        step = 0

        history = []

        # Save initial observation
        info['stepsSinceLastReset'] = step
        history.append(info.copy())

        # Run each action in the gold path
        for actionToTake in goldPath:
            print("Next gold action: " + actionToTake)

            # Take a step in the environment
            # First, check to see if the command is intended for a module
            moduleWasRun, moduleResult = moduleInterface.runCommand(actionToTake)
            if (moduleWasRun == True):
                # Symbolic module was run -- add result to current 'info'
                #print("Info (before): ")
                #print(info)
                info = addModuleResultToInfo(lastRawInfo, moduleResult, actionToTake)
                lastRawInfo['lastActionStr'] = ""
                #print("Info (after): ")
                #print(info)

            else:
                # Command was not intended for symbolic module -- run environment
                _, _, _, info = env.step(actionToTake)
                lastRawInfo = info.copy()

            # Give modules new observations
            moduleInterface.giveEnvironmentStatus(lastRawInfo['observation'], lastRawInfo['inventory'], lastRawInfo['look'])

            # Sanitize info, and add in module commands to valid actions
            info = sanitizeInfo(info, moduleInterface)
            obs = info['obs']
            reward = info['reward']
            done = info['done']
            score = info['score']

            # Save history
            info['stepsSinceLastReset'] = step
            history.append(info.copy())

            print("Obs: " + obs)
            print(f"Variation: {variationIdx}, Step: {step}, Score: {score}, Action: {actionToTake}")
            print("")
            step += 1


        # Store history
        # Get history internally (keeps track of module commands)
        finalScore = 0
        if (len(history) > 0):
            finalScore = history[-1]['score']

        runHistory = {
            'finalScore': finalScore,
            'history': history,
        }

        histories.append(runHistory)

        # TODO: Check that score is 1.0
        if (score < 1.0):
            warningStr = "WARNING: Score for this variation (" + str(variationIdx) + ") is less than 1.0.  This may be an error in the gold path."
            print(warningStr)
            errors.append(warningStr)

        print("Run completed...")

    # If there were any warnings/errors, print these out at the end so they're easily visible to the user
    if (len(errors) > 0):
        print ("Warnings/Errors: " + str(errors))
        print ("\n".join(errors))

    # Return the histories/trajectories from running the gold paths:
    return histories



# Build a set of (source, target) strings for T5 to learn, from a history
def mkSourceTargetStrsFromHistory(oneHistory, args):
    # NOTE: The action that should be taken at *THIS* step is stored as the lastActionStr for the *NEXT* step
    out = []

    history = oneHistory['history']
    for stepNum in range(0, len(history)):
        historyStep = history[stepNum]

        print(json.dumps(historyStep, indent=4, sort_keys=True))
        task_description = historyStep['taskDesc']
        obs = historyStep['obs']
        look = historyStep['look']
        inv = historyStep['inv']
        score = historyStep['score']

        # Previous observation
        prev_obs = ""
        if (stepNum > 0):
            prev_obs = history[stepNum-1]['obs']

        # Previous action -- note, could be either proper action or module command (either one could be populated)
        prev_action = historyStep['lastActionStr']
        if (len(prev_action) < 1):
            if ('moduleCommand' in historyStep):
                prev_action = historyStep['moduleCommand']

        # Generate source string
        sourceStr = ""
        if (args["mode"] == "bc"):
            print ("MODE: Behavior Cloning")
            sourceStr = build_input_str_behavior_cloning(task_description, prev_obs, prev_action, obs, look, inv)
        elif (args["mode"] == "dt"):
            print ("MODE: Decision Transformer")
            sourceStr = build_input_str_decision_transformer(task_description, prev_obs, prev_action, obs, look, inv, score)
        else:
            print("Unknown mode: " + str(args["mode"]))
            exit(1)

        # Generate target string (the next action the agent should choose)
        targetStr = "completed"
        if (stepNum < len(history) - 1):
            targetStr = history[stepNum+1]['lastActionStr']
            # NOTE: If the last action is blank, then it was likely a module command -- use the module command instead, if it exists.
            if (len(targetStr) < 1):
                if ('moduleCommand' in history[stepNum+1]):
                    targetStr = history[stepNum+1]['moduleCommand']

        # Pack
        packed = {
            "source": sourceStr,
            "target": targetStr
        }

        # Store
        out.append(packed)

    # Return the history converted to source/target strings
    return out


# Main function for generating training data and exporting it to a file (to use for training the T5 agent, using an external fine tuning script)
def generateTrainingData(args):
    # Step 1: Run the gold paths in from the training set, to generate training data
    histories = None
    if (args["game_name"] == "arithmetic"):
        histories = runGoldPathsArithmetic(args)
    elif (args["game_name"].startswith("mapreader")):
        histories = runGoldPathsMapReader(args)
    elif (args["game_name"] == "sorting"):
        histories = runGoldPathsSorting(args)
    elif (args["game_name"] == "twc"):
        histories = runGoldPathsTWC(args)
    else:
        print("ERROR: This game (" + args["game_name"] + ") is not currently supported for T5 gold path generation.")
        exit(1)

    print("")
    print( json.dumps(histories, indent=4, sort_keys=True) )

    # Step 2: Convert the histories to source/target strings
    sourceTargetOut = []
    for oneRun in histories:
        print("----")
        sourceTargetStrs = mkSourceTargetStrsFromHistory(oneRun, args)
        print(json.dumps(sourceTargetStrs, indent=4, sort_keys=True))
        sourceTargetOut.extend(sourceTargetStrs)

    # Step 3: Export source/target out to file
    numEpsiodes = len(histories)
    filenameOut = args["traindataSavePrefix"] + "-game" + args["game_name"] + "-numepisodes" + str(numEpsiodes) + "." + str(args["set"]) + ".sourcetarget.json"
    print("Exporting JSON lines file for T5 trainer: " + filenameOut)
    fp = open(filenameOut, "w")
    for stOut in sourceTargetOut:
        fp.write( json.dumps(stOut) + "\n" )
    fp.close()
    print("Export completed.")


#
#   T5 Agent (running/evaluation)
#

# Example user input console, to play through a game.
def T5Agent(args):
    gameName = args["game_name"]
    enabledModules = args["useSymbolicModules"]
    lm = args["lm_path"]
    setName = args["set"]
    verboseFilenameOut = "resultsout-" + gameName + "-mod" + enabledModules + str(enabledModules) + "-lm" + str(lm).replace("/", "_") + "-set" + setName + ".json"

    # Initialize the environment
    env = initializeEnv(threadNum=3, args=args)

    # Initialize the language model
    lm_model = T5ForConditionalGeneration.from_pretrained(args["lm_path"]).eval()

    num_layers = len(lm_model.encoder.block)
    mp_size = args["model_parallelism_size"]
    layers_per_device = ceil(num_layers/mp_size)

    device_map = {i: list(range(i*layers_per_device, min((i+1)*layers_per_device, num_layers))) for i in range(mp_size)}
    print("Device map: ")
    print(device_map)


    # device_map = {0: [0, 1, 2, 3, 4, 5, 6, 7],
    #               1: [8, 9, 10, 11, 12, 13, 14, 15],
    #               2: [16, 17, 18, 19, 20, 21, 22, 23]}

    lm_model.parallelize(device_map)
    tokenizer = T5Tokenizer.from_pretrained(args["lm_path"])

    # Pick which set to evaluate on
    variations = []
    if (args["set"] == "train"):
        variations = list(env.getValidSeedsTrain())
    elif (args["set"] == "dev"):
        variations = list(env.getValidSeedsDev())
    elif (args["set"] == "test"):
        variations = list(env.getValidSeedsTest())
    else:
        print("ERROR: Unknown set to evaluate on (" + str(args["set"]) + ")")
        exit(1)

    # History saver
    bufferedHistorySaver = BufferedHistorySaver(filenameOutPrefix = args["historySavePrefix"] + "-game" + str(args["game_name"]) + "-lm" + str(lm).replace("/", "_") + "-" + str(args["set"]))

    # Log output prefix
    if (len(args["output_path"]) > 0):
        args["output_path"] = args["output_path"] + "/"

        # Make path if it doesn't exist
        if (not os.path.exists(args['output_path'])):
            os.makedirs(args["output_path"])

    if args["lm_path"].endswith('/'):
        args["lm_path"] = args["lm_path"][:-1]

    filenameOutPrefix = args["output_path"] + "transformer-" + args["mode"] + "-eval-" + str(args["lm_path"].split('/')[-1]) + "-task" + str(args['game_name'])


    scores = []
    totalSteps = []
    totalEnvSteps = []
    totalModuleSteps = []

    # Determine a (sub)set of variations to run
    maxVariations = args['num_variations']
    if (len(variations) > maxVariations):
        print("NOTE: More than " + str(maxVariations) + " variations.  Only evaluating 100.")
        variations = variations[:maxVariations]


    for variationIdx in variations:

        # Reset with this new variation(seed), based on the set
        obs = ""
        moduleInterface = None
        if (args["set"] == "train"):
            info, moduleInterface = resetWithVariationTrain(env, args, variationIdx)
        elif (args["set"] == "dev"):
            info, moduleInterface = resetWithVariationDev(env, args, variationIdx)
        elif (args["set"] == "test"):
            info, moduleInterface = resetWithVariationTest(env, args, variationIdx)
        else:
            print("ERROR: Unrecognized set to evaluate on (" + str(args["set"]) + ")")
            exit(1)

        # Give modules initial observations
        print(type(info))
        print(info)


        moduleInterface.giveEnvironmentStatus(info['observation'], info['inventory'], info['look'])
        # Sanitize info, and add in module commands to valid actions
        lastRawInfo = info          # lastRawInfo should be unsanitized version?
        info = sanitizeInfo(info, moduleInterface)

        task_description = info['taskDescription']
        prev_obs = ''
        prev_action = ''



        done = False
        score = 0.0
        step = 0

        # The env has an internal step count, some actions like look around are free
        # however, the t5 model only generates the action "look around", which will result in a dead loop below
        # so the max_steps here is only used to avoid the model generating the same action forever
        max_steps = args["max_steps"] #* 2

        lastNActions = []
        history = []

        # Save initial observation
        info['stepsSinceLastReset'] = step
        history.append(info.copy())

        # Trying to set this up to match what the histories look like when they're saved, so the source->target between train/eval look identical.
        obs = info['obs']
        done = info['done']
        score = info['score']
        prev_obs = obs              # This looks like a bug in the training code (that sets prev_obs to the same value as obs for the first iteration) -- but repeating it here.
        prev_action = ""
        actionToTake = ""

        while not done:
            print("\n----------------------------------------------------------------------------------------------------\n")
            input_str = ""
            prev_action = lastNActions[-1] if len(lastNActions) > 0 else ""

            if (args["mode"] == "bc"):
                print ("MODE: Behavior Cloning")
                input_str = build_input_str_behavior_cloning(task_description, prev_obs, prev_action, obs, info['look'], info['inv'])
            elif (args["mode"] == "dt"):
                print ("MODE: Decision Transformer")
                input_str = build_input_str_decision_transformer(task_description, prev_obs, prev_action, obs, info['look'], info['inv'], info['score'])
            else:
                print("Unknown mode: " + str(args["mode"]))
                exit(1)

            print("* InputStr: " + input_str)
            input_ids = tokenizer(input_str, return_tensors="pt", truncation=True).input_ids

            # Generate a list of candidate possible next actions
            sample_outputs = lm_model.generate(
                input_ids.to(device),
                max_length=50,
                diversity_penalty=0.9,                      ## Needs to be tuned to the task
                num_return_sequences=args['beams'],
                num_beams=args['beams'],
                num_beam_groups=args['beams'],
            )
            lm_pred = sample_outputs
            lm_pred_text = tokenizer.decode(lm_pred[0])

            # Take the first prediction that is not "look around"
            print("Top N Predictions:")
            useAction = ""
            predStrs = []
            for i, pred in enumerate(lm_pred):
                text = tokenizer.decode(pred)
                text = post_process_generation(text)
                if ((len(useAction) == 0) and (text.strip() != "look around")):
                    useAction = text
                print("\t" + str(i) + "\t" + str(text) )
                predStrs.append(text)

            #print(lm_pred_text)

            # Get valid actions at this point
            prev_action = actionToTake
            validActions = info['valid']
            getBestValidAction = findValidAction(predStrs, validActions, lastNActions)
            actionToTake = getBestValidAction
            print ("Valid actions: " + str(validActions))
            print ("Best action: " + str(actionToTake))

            # Take a step in the environment
            # First, check to see if the command is intended for a module
            moduleWasRun, moduleResult = moduleInterface.runCommand(actionToTake)
            if (moduleWasRun == True):
                # Symbolic module was run -- add result to current 'info'
                #print("Info (before): ")
                #print(info)
                info = addModuleResultToInfo(lastRawInfo, moduleResult, actionToTake)
                lastRawInfo['lastActionStr'] = ""
                #print("Info (after): ")
                #print(info)

            else:
                # Command was not intended for symbolic module -- run environment
                _, _, _, info = env.step(actionToTake) # New API -- now returns a tuple
                lastRawInfo = info

            # Give modules observations from environment
            #print("lastRawInfo:")
            #print(lastRawInfo)
            moduleInterface.giveEnvironmentStatus(lastRawInfo['observation'], lastRawInfo['inventory'], lastRawInfo['look'])
            # Sanitize info, and add in module commands to valid actions
            info = sanitizeInfo(info, moduleInterface)

            # Store last observation/action
            prev_obs = obs


            obs = info['obs']
            reward = info['reward']
            done = info['done']
            score = info['score']

            #obs, reward, done, info = env.step(action)
            #score = info['score']
            #if score < 0:
            #    done = True
            #    score = 0

            # Save history
            info['stepsSinceLastReset'] = step
            history.append(info.copy())


            print("Obs: " + obs)
            #print("Input string: " + str(input_str))
            print(f"Variation: {variationIdx}, Step: {step}, Score: {score}, Action: {actionToTake}")
            print("")
            step += 1
            if (step >= max_steps):
                print("Maximum steps exceeded (" + str(step) + ").")
                break
            if done:
                print("Received 'done' signal from environment.")
                break

            lastNActions.append(actionToTake)
            if (len(lastNActions) > 3):
                lastNActions = lastNActions[-4:]

            print("LastNActions: " + str(lastNActions))

            # Early stopping if we're in a loop
            if (len(lastNActions) >= 4):
                if (len(set(lastNActions)) == 1):
                    print("All actions in history are the same -- model is likely in a loop, stopping early.")
                    break

        # Store history
        # Get history internally (keeps track of module commands)
        finalScore = 0
        if (len(history) > 0):
            finalScore = history[-1]['score']

        runHistory = {
            'finalScore': finalScore,
            'history': history,
        }

        bufferedHistorySaver.storeRunHistory(runHistory, variationIdx, notes={'step':step})
        bufferedHistorySaver.saveRunHistoriesBufferIfFull(maxPerFile=args["maxHistoriesPerFile"])

        # Save scores (clip negative scores to 0, for averaging)
        if (score < 0):
            score = 0.0
        scores.append(score)

        # Save total number of steps
        totalSteps.append(len(history))

        # Total number of environment steps
        envSteps = len([x for x in history if len(x['lastActionStr']) > 0])
        moduleSteps = len([x for x in history if len(x['moduleCommand']) > 0])
        totalEnvSteps.append(envSteps)
        totalModuleSteps.append(moduleSteps)

        print("Run completed...")
        print("Scores: " + str(scores))
        print("Steps: " + str(totalSteps))
        print("Steps (Env): " + str(totalEnvSteps))
        print("Steps (Mod): " + str(totalModuleSteps))
        time.sleep(2)

    # Episodes are finished -- manually save any last histories still in the buffer
    bufferedHistorySaver.saveRunHistoriesBufferIfFull(maxPerFile=args["maxHistoriesPerFile"], forceSave=True)

    avgScore = sum(scores) / len(scores)
    print("Average score: " + str(avgScore))

    avgSteps = sum(totalSteps) / len(totalSteps)
    print("Average steps: " + str(avgSteps))

    avgEnvSteps = sum(totalEnvSteps) / len(totalEnvSteps)
    print("Average steps (env): " + str(avgEnvSteps))

    avgModSteps = sum(totalModuleSteps) / len(totalModuleSteps)
    print("Average steps (mod): " + str(avgModSteps))

    # Save to file
    scoresPacked = {
        'setName': setName,
        'lm': lm,
        'gameName:': gameName,
        'enabledModules': enabledModules,
        'scores': scores,
        'totalSteps': totalSteps,
        'totalEnvSteps': totalEnvSteps,
        'totalModuleSteps': totalModuleSteps,
        'avgScore': avgScore,
        'avgSteps': avgSteps,
        'avgEnvSteps': avgEnvSteps,
        'avgModSteps': avgModSteps,
        'numSamples': len(scores),
    }

    print("Saving " + str(verboseFilenameOut))
    with open(verboseFilenameOut, "w") as write_file:
        json.dump(scoresPacked, write_file, indent=4)

    #print("Shutting down server...")
    #env.shutdown()     # No longer required with new TWX API?

    print("Completed.")



def parse_args():
    parser = argparse.ArgumentParser()
    #parser.add_argument("--jar_path", type=str)
    #parser.add_argument("--task_num", type=int, default=0)
    parser.add_argument("--max_steps", type=int, default=50)
    parser.add_argument("--lm_path", default="lm_model")
    parser.add_argument("--simplification_str", default="easy")
    parser.add_argument("--beams", type=int, default=16)
    #parser.add_argument("--max_episode_per_file", type=int, default=1000)
    parser.add_argument("--mode", default="bc")
    parser.add_argument("--set", default="dev")
    parser.add_argument("--output_path", default="")
    parser.add_argument("--model_parallelism_size", type=int, default=1)    # the number of GPUs.

    parser.add_argument('--historySavePrefix', default='t5saveout', type=str)
    parser.add_argument('--maxHistoriesPerFile', default=1000, type=int)

    # Number of variations to run
    parser.add_argument("--num_variations", type=int, default=100)

    # TextWorldExpress
    parser.add_argument("--jar_path", type=str,
                        help="Path to the TextWorldExpress jar file. Default: use builtin.")
    parser.add_argument("--game_name", type=str, choices=['arithmetic', 'twc', 'mapreader', 'sorting', 'twc-easy'], default='arithmetic',
                        help="Specify the game to play. Default: %(default)s")
    parser.add_argument("--game_params", type=str, default='',
                        help="TODO: This currently is not supported")


    # Mode select: Training data generation, OR running the model.
    parser.add_argument("--train_or_eval", type=str, choices=['train-gen', 'eval'], default='eval',
                        help="Specify whether to generate training data, evaluate the model. Default: %(default)s")

    parser.add_argument('--traindataSavePrefix', default='t5goldout', type=str)
    parser.add_argument('--useSymbolicModules', default='', type=str)

    args = parser.parse_args()
    params = vars(args)

    # Post-processing
    params['game_params'] = ""

    if (params['game_name'] == "twc-easy"):
        params['game_name'] = "twc"
        paramStr = "numLocations=1,numItemsToPutAway=1,includeDoors=0,limitInventorySize=0"     # Equivalent of TWC-Easy
        params['game_params'] = paramStr

    return params


#
#   Main
#
def main():
    args = parse_args()

    if (args['train_or_eval'] == "train-gen"):
        generateTrainingData(args)
    elif (args['train_or_eval'] == "eval"):
        T5Agent(args)
    else:
        raise Exception("Invalid train_or_eval mode: " + args['train_or_eval'])

if __name__ == "__main__":
    main()
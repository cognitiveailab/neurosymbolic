import sys
import random
import argparse

from textworld_express import TextWorldExpressEnv
from symbolicModule import *


try:
    # For command line history and autocompletion.
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.history import InMemoryHistory
    prompt_toolkit_available = sys.stdout.isatty()
except ImportError:
    pass

try:
    # For command line history when prompt_toolkit is not available.
    import readline  # noqa: F401
except ImportError:
    pass


# Append the result of the module as an observation
def addModuleResultToInfo(infoIn, moduleResult, moduleCommand):
    infoIn['obs'] = moduleResult
    infoIn['observation'] = moduleResult
    infoIn['moduleCommand'] = moduleCommand
    return infoIn


def userConsole(args):
    """ Example user input console, to play through a game. """
    history = None
    if prompt_toolkit_available:
        history = InMemoryHistory()

    exitCommands = ["quit", "exit"]

    gameName = args['game_name']

    # Initialize environment
    env = TextWorldExpressEnv(args['jar_path'], envStepLimit=args['max_steps'], threadNum=0)
    gameNames = env.getGameNames()
    print("Supported Game Names: " + str(gameNames))

    # Load the task
    gameFold = "train"
    gameSeed = args['seed']
    gameParams = args['gameParams']  #     # e.g. "numLocations=5, includeDoors=1"
    print("Game Params: " + gameParams)
    generateGoldPath = True
    env.load(gameName, gameFold, gameSeed, gameParams, generateGoldPath)

    print("Selected Game: " + str(gameName))
    print("Generation properties: " + str(env.getGenerationProperties()) )

    if (generateGoldPath == True):
        print("Gold path: " + str(env.getGoldActionSequence()))

    # Initialize a random task variation in this set
    info = env.resetWithSeed(gameSeed, gameFold, generateGoldPath)
    lastRawInfo = info

    # Module interface
    #enabledModules = ["calc"]       # TODO: Read from list
    #enabledModules = ["navigation"]       # TODO: Read from list
    enabledModules = ["kb-twc"]       # TODO: Read from list
    #enabledModules = []       # TODO: Read from list
    properties = env.getGenerationProperties()
    moduleInterface = SymbolicModuleInterface(enabledModules, properties)
    
    # Give modules initial observations
    moduleInterface.giveEnvironmentStatus(info['observation'], info['inventory'], info['look'])    

    # Task description
    print("Task Description: " + env.getTaskDescription())
    print("")
    
    # Take action
    curIter = 0    

    userInputStr = ""
    print("\nType 'exit' to quit.\n")    
    
    while (userInputStr not in exitCommands):

        # Select a random action
        validActions = info['validActions']

        # Verbose output mode
        print("")
        print("Step " + str(curIter))
        print(str(info['observation']))
        print("Score: " + str(info['scoreRaw']) + " (raw)    " + str(info['score']) + " (normalized)")
        print("Reward: " + str(info['reward']))
        #print("Valid Actions: " + str(validActions))

        if (info['tasksuccess'] == True):
            print("Task Success!")
        if (info['taskfailure'] == True):
            print("Task Failure!")

            

        # Get user input
        #if prompt_toolkit_available:
        #    actions_completer = WordCompleter(validActions, ignore_case=True, sentence=True)
        #    userInputStr = prompt('> ', completer=actions_completer,
        #                          history=history, enable_history_search=True)
        #else:
        print("Valid Actions: " + str(validActions))
        print("Module actions: " + str(moduleInterface.getValidCommands()))
        userInputStr = input('> ')


        # Sanitize input
        userInputStr = userInputStr.lower().strip()

        # Take action
        #obs = env.step(userInputStr)

        # First, check to see if the command is intended for a module
        moduleWasRun, moduleResult = moduleInterface.runCommand(userInputStr)
        if (moduleWasRun == True):
            # Symbolic module was run -- add result to current 'info'
            #print("Info (before): ")
            #print(info)
            info = addModuleResultToInfo(lastRawInfo, moduleResult, userInputStr)
            lastRawInfo['lastActionStr'] = ""
            #print("Result from module: ")
            #print(moduleResult)

        else:
            # Command was not intended for symbolic module -- run environment
            info = env.step(userInputStr)
            lastRawInfo = info


        # Give modules new observations    
        moduleInterface.giveEnvironmentStatus(lastRawInfo['observation'], lastRawInfo['inventory'], lastRawInfo['look'])



        curIter += 1

    print("Completed.")

    #print("Run History:")
    #print(env.getRunHistory())

    print("Shutting down server...")
    env.shutdown()



#
#   Parse command line arguments
#
def parse_args():
    desc = "Run a model that chooses random actions until successfully reaching the goal."
    parser = argparse.ArgumentParser(desc)
    parser.add_argument("--jar_path", type=str,
                        help="Path to the ScienceWorld jar file. Default: use builtin.")
    parser.add_argument("--game-name", type=str, choices=['cookingworld', 'coin', 'twc', 'mapreader', 'arithmetic', 'takethisaction', 'simonsays', 'sorting', 'twc-easy'], default='cookingworld',
                        help="Specify the game to play. Default: %(default)s")
    parser.add_argument("--game-fold", type=str, choices=['train', 'dev', 'test'], default='train',
                        help="Specify the game set to use (train, dev, test). Default: %(default)s")
    parser.add_argument("--max-steps", type=int, default=50,
                        help="Maximum number of steps per episode. Default: %(default)s")
    parser.add_argument("--seed", type=int, default=0,
                        help="Seed the generator for used in generating the game")

    args = parser.parse_args()
    params = vars(args)


    # Post-processing
    params['gameParams'] = ""

    if (params['game_name'] == "twc-easy"):
        params['game_name'] = "twc"
        paramStr = "numLocations=1,numItemsToPutAway=1,includeDoors=0,limitInventorySize=0"     # Equivalent of TWC-Easy
        params['gameParams'] = paramStr    


    return params


def main():
    print("TextWorldExpress 1.0 API Examples - Human User Console")

    # Parse command line arguments
    args = parse_args()
    random.seed(args["seed"])
    userConsole(args)

if __name__ == "__main__":
    main()

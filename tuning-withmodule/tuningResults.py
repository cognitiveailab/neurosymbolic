# tuningResults.py

import json


def getScores(filename):
    with open(filename) as f:
        data = json.load(f)
    return data



#
#   Main
#

gameNames = ["arithmetic", "mapreader", "sorting", "twc"]

epValues = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

print("Tuning Results:")
for gameName in gameNames:
    print("")
    print(gameName)
    print("Train Epochs \tScore (dev)\tNumSamples")
    for ep in epValues:
        # example: resultsout-sorting-mod-lmt5twx-game-sorting-nomodule-base-1024-ep12-setdev.json
        filename = ""
        if (gameName == "arithmetic"):
            filename = "resultsout-" + gameName + "-modcalccalc-lmt5twx-game-" + gameName + "-withcalcmodule-base-1024-ep" + str(ep) + "-setdev.json"
        elif (gameName == "mapreader"):
            filename = "resultsout-" + gameName + "-modnavigationnavigation-lmt5twx-game-" + gameName + "-withnavmodule-base-1024-ep" + str(ep) + "-setdev.json"
        elif (gameName == "sorting"):
            filename = "resultsout-" + gameName + "-modsortquantitysortquantity-lmt5twx-game-" + gameName + "-withsortmodule-base-1024-ep" + str(ep) + "-setdev.json"
        elif (gameName == "twc"):
            filename = "resultsout-" + gameName + "-modkb-twckb-twc-lmt5twx-game-" + gameName + "-withtwcmodule-base-1024-ep" + str(ep) + "-setdev.json"
        else:
            print("ERROR: Unknown game name (" + str(gameName) + ")")
        scoreData = getScores(filename)

        avgScore = scoreData['avgScore']
        avgEnvSteps = scoreData['avgEnvSteps']
        numSamples = scoreData['numSamples']

        print(str(ep) + "        \t" + "{:.3f}".format(avgScore) + "      \t" + str(numSamples))

    print("----------------------------------------------------")
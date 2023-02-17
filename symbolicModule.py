# Symbolic Module Interface
from cgitb import reset
import itertools
from operator import mod
import re
import csv
import spacy

nlp = spacy.load("en_core_web_sm")

class SymbolicModuleInterface:

    #
    #   Constructor
    #
    def __init__(self, enabledModules, properties):
        self.modules = []
        self.properties = properties

        # Add requested modules
        for moduleName in enabledModules:
            self.addModule(moduleName)

    #
    #   Enabling modules
    #
    def addModule(self, moduleName):
        if (moduleName == "calc"):
            print("Adding calc module")
            self.modules.append( ModuleCalc(self.properties) )
        elif (moduleName == "navigation"):
            print("Adding navigation module")
            self.modules.append( ModuleNavigation(self.properties) )
        elif (moduleName == "sortquantity"):
            print("Adding quantity sorting module")
            self.modules.append( ModuleSortByQuantity(self.properties) )
        elif (moduleName == "kb-twc"):
            print("Adding knowledge base module (TWC)")
            self.modules.append( ModuleKnowledgeBaseTWC(self.properties) )

        else:
            print("ERROR: Unknown module name: " + moduleName)

    # Get a list of all enabled modules
    def getEnabledModuleNames(self):
        return [module.moduleName for module in self.modules]

    #
    #   Getting lists of valid commands from modules
    #
    def getValidCommands(self):
        out = []        
        for module in self.modules:            
            out.extend(module.getValidCommands())

        return out

    #
    #   Updating modules with the current environment status
    #
    def giveEnvironmentStatus(self, observationStr, invStr, freelookStr):
        for module in self.modules:
            module.scrapeObservationStr(observationStr)
            module.scrapeInventoryStr(invStr)
            module.scrapeFreeLookStr(freelookStr)


    #
    #   Get the result of a command 
    #
    # Returns (success, result). 
    # If success is False, then there is no module with the requested command as a valid command.
    def runCommand(self, actionStr):
        for module in self.modules:
            if (module.isValidCommand(actionStr)):
                return (True, module.runCommand(actionStr))

        return (False, "")



# Template for a module
class SymbolicModule:

    #
    #   Constructor
    #
    def __init__(self, properties):
        self.moduleName = "ModuleTemplate"
        self.properties = properties
        

    #
    #   Valid commands
    #

    # Get a list of valid actions from this module
    def getValidCommands(self):
        return []

    # Returns True if the action is valid for this module
    def isValidCommand(self, actionStr):
        if (actionStr in self.getValidCommands()):
            return True
        else:
            return False

    #
    #   Observation scraping
    #
    def scrapeObservationStr(self, observationStr):
        pass

    def scrapeInventoryStr(self, inventoryStr):
        pass    

    def scrapeFreeLookStr(self, freeLookStr):
        pass

    #
    #   Command Runner
    #
    def runCommand(self, actionStr):
        # Check that this is a valid action
        if (self.isValidAction(actionStr) == False):
            return "This is not a valid action for this module (" + self.moduleName + ", " + actionStr + ")"

        # Run the action
        return ""



#
#   Calculator module
#
class ModuleCalc(SymbolicModule):

    #
    #   Constructor
    #
    def __init__(self, properties):
        self.moduleName = "calc"
        self.properties = properties

        # Extract the valid arguments for this module
        self.validCalcArguments = []
        self.validCalcArguments.append( self.properties['hidden_num1'] )
        self.validCalcArguments.append( self.properties['hidden_num2'] )
        
        # A list of the valid operations that this module can perform
        self.validOperations = ["add", "sub", "mul", "div"]

    #
    #   Valid Commands
    #
    def getValidCommands(self):
        out = []        
        for opStr in self.validOperations:
            for args in itertools.permutations(self.validCalcArguments, 2):
                out.append( opStr + " " + str(args[0]) + " " + str(args[1]) )

        return out


    #
    #   Run Command
    #
    def runCommand(self, actionStr):
        # Check that this is a valid action
        if (self.isValidCommand(actionStr) == False):
            return "This is not a valid action for this module (" + self.moduleName + ", " + actionStr + ")"

        #print("(MODULE " + self.moduleName + "): Running command: " + actionStr)

        # Split the action into the operation and the arguments
        opStr, arg1, arg2 = actionStr.split(" ")
        op = None
        if (opStr == "add"):
            result = int(arg1) + int(arg2)
            return "The result of adding " + str(arg1) + " and " + str(arg2) + " is " + str(result)
        elif (opStr == "sub"):
            result = int(arg1) - int(arg2)
            return "The result of subtracting " + str(arg2) + " from " + str(arg2) + " is " + str(result)
        elif (opStr == "mul"):
            result = int(arg1) * int(arg2)
            return "The result of multiplying " + str(arg1) + " and " + str(arg2) + " is " + str(result)
        elif (opStr == "div"):
            result = int(arg2) / int(arg1)
            return "The result of dividing " + str(arg2) + " by " + str(arg1) + " is " + str(result)

        # Default return
        return "This is not a valid operation for this module (" + self.moduleName + ", " + opStr + ")"


#
#   Map Reading/Navigation module
#
class ModuleNavigation(SymbolicModule):

    #
    #   Constructor
    #
    def __init__(self, properties):
        self.moduleName = "navigation"
        self.properties = properties

        # Extract the valid arguments for this module
        #self.validCalcArguments = []
        #self.validCalcArguments.append( self.properties['hidden_num1'] )
        #elf.validCalcArguments.append( self.properties['hidden_num2'] )        
        # A list of the valid operations that this module can perform        

        # Map edges
        self.mapEdges = []

        # Current location (blank if unknown)
        self.currentLocation = ""


    #
    #   Valid Commands
    #
    def getValidCommands(self):
        out = []        
        knownLocations = self.getLocations()

        # Command 1: Path from X to Y        
        #for args in itertools.permutations(knownLocations, 2):
        #    out.append("path from " + str(args[0]) + " to " + str(args[1]) )

        # Command 2: Path from current location to Y
        #for arg in knownLocations:
        #    out.append("path to " + arg)

        # command 3: Next step from current location to Y
        for arg in knownLocations:
            out.append("next step to " + arg)

        return out


    #
    #   Run Command
    #
    def runCommand(self, actionStr):
        # Check that this is a valid action
        if (self.isValidCommand(actionStr) == False):
            return "This is not a valid action for this module (" + self.moduleName + ", " + actionStr + ")"

        arg1 = ""
        arg2 = ""                

        # Parse the arguments: split the action into the operation and the arguments
        fields = actionStr.split(" ")
        if (actionStr.startswith("path from ")):            
            opStr = "path from"
            args = actionStr[len("path from"):].strip().split(" to ")        
            arg1 = args[0].strip()
            arg2 = args[1].strip()
        elif (actionStr.startswith("path to ")):
            opStr = "path to"
            arg1 = actionStr[len("path to"):].strip()
        elif (actionStr.startswith("next step to ")):
            opStr = "next step to"
            arg1 = actionStr[len("next step to"):].strip()
        else:
            return "This is not a valid action for this module (" + self.moduleName + ", " + actionStr + ")"

        # Step 2: Perform the path operation
        if (opStr == "path from"):
            return self.getPathFromXToYCommand(arg1, arg2)
        elif (opStr == "path to"):
            return self.getPathToYCommand(arg1)
        elif (opStr == "next step to"):
            return self.getNextStepToYCommand(arg1)

        # Default return
        return "This is not a valid operation for this module (" + self.moduleName + ", " + opStr + ")"


    #
    #   Map Pathfinding
    #
    def findPath(self, startLoc, goalLoc):
        MAX_ITER = 10
        pathPool = [ [startLoc] ]

        startLoc = startLoc.lower().strip()
        goalLoc = goalLoc.lower().strip()

        # Edge case: Check if the start and end locations are the same
        if (startLoc == goalLoc):
            return (True, [])

        # Iteratively assemble possible paths
        numIter = 0        
        while (numIter < MAX_ITER):
            # Step 1: Find the next location for each path
            newPathPool = []
            for path in pathPool:
                lastLoc = path[-1]

                # Get connections
                connections = self.getConnections(lastLoc)

                # Add every connection to this location
                for connection in connections:
                    newPath = path[:]
                    newPath.append(connection)
                    newPathPool.append(newPath)

                    # Winning condition: Check if the last location is the goal location
                    if (connection == goalLoc):
                        return (True, newPath)

            # Step 2: Once we've made all the pools, swap the old pool with the new one
            pathPool = newPathPool
            
            # Keep track of the number of iterations
            numIter += 1

        # If we've reached this point, we've failed to find a path
        return (False, [])


    # Add an edge to the map
    def addEdge(self, location1, location2):
        location1 = location1.lower().strip()
        location2 = location2.lower().strip()

        #print("Adding " + location1 + " / " + location2)
        self.mapEdges.append( (location1, location2) )
        self.mapEdges.append( (location2, location1) )
        self.mapEdges = list(set(self.mapEdges))

    # Get a list of locations that connect to a given location
    def getConnections(self, location):
        out = []
        for edge in self.mapEdges:
            if (edge[0] == location):
                out.append(edge[1])

        return out

    # Get a list of locations
    def getLocations(self):
        out = []
        for edge in self.mapEdges:
            out.append(edge[0])
            out.append(edge[1])
        
        return list(set(out))


    # Scrape observation for map related information
    def scrapeObservationStr(self, observationStr):
        # Case 1: Check for whole maps
        if (observationStr.startswith("The map reads:")):
            # Split the map into lines
            lines = observationStr.split("\n")
            for line in lines:
                if ("connects to the" in line):
                    fields = line.split(" connects to the ")
                    # print ("Fields: " + str(fields))
                    if (len(fields) >= 2):
                        startLocation = fields[0]
                        endLocations = re.split(',|and', fields[1])

                        startLocationStr = self.trimStopWords(startLocation)
                        for endLocation in endLocations:
                            endLocationStr = self.trimStopWords(endLocation)
                            self.addEdge(startLocationStr, endLocationStr)

        # Case 2: Room
        if (observationStr.startswith("You are in the")):
            curLoc = ""
            sents = observationStr.split(".")
            for sent in sents:
                #print("Sent: " + sent)
                if (sent.startswith("You are in the")):
                    fields = sent.split("You are in the ")
                    #print("Fields: " + str(fields))
                    curLoc = self.trimStopWords( fields[1] )

            #print("CurLoc: " + str(curLoc))
            
            if (len(curLoc) > 0):
                for sent in sents:
                    sent = sent.strip()
                    if (sent.strip().startswith("To the")):
                        split = re.split("To the|you see the|is the", sent.strip())
                        #print("Split: " + str(split))
                        if (len(split) == 3):
                            loc = split[-1]
                            sanitizedEndLoc = self.trimStopWords(loc)
                            if (len(sanitizedEndLoc) > 0):
                                self.addEdge(curLoc, sanitizedEndLoc)

                # Also store the current location, for the agent navigation commands
                self.currentLocation = curLoc


    # Trim stop words from a short location name
    def trimStopWords(self, strIn):
        stopWords = ["a", "an", "the", "."]
        #print("strIn: " + str(strIn))
        sanitizedStr = re.sub("[^\w\s]", " ", strIn)
        tokens = sanitizedStr.split(" ")        
        out = []
        for token in tokens:
            sanitizedToken = token.strip()
            if ((len(sanitizedToken) > 0) and (token.lower() not in stopWords)):
                out.append(sanitizedToken)

        outStr = " ".join(out)
        outStr = outStr.strip()
        return outStr


    #
    #   Commands
    #

    # Get directions from a given location, to a given location.  Returns the full path (list of locations). 
    def getPathFromXToYCommand(self, startLocation, endLocation):
        success, path = self.findPath(startLocation, endLocation)
        if (success == False) or (len(path) == 0):
            return "I couldn't find a path from " + startLocation + " to " + endLocation + "."

        # If the path length is 1, then the agent is already at the current location
        if (len(path) == 1):
            return "You are already at " + endLocation + "."

        # Trim off the first location in the path, since it's the current location
        path = path[1:]
        return "The path to reach the " + endLocation + " is: " + ", ".join(path) + "."
    
    # Get directions from self.currentLocation to a given location.  Returns the full path (list of locations).
    def getPathToYCommand(self, endLocation):
        if (len(self.currentLocation) == 0):
            return "I'm not sure what your current location is right now."

        return self.getPathFromXToYCommand(self.currentLocation, endLocation)

    # Gets the next location to move to, on the path to move from the current location to endLocation.
    def getNextStepToYCommand(self, endLocation):
        startLocation = self.currentLocation
        success, path = self.findPath(startLocation, endLocation)
        if (success == False) or (len(path) == 0):
            return "I couldn't find a path from " + startLocation + " to " + endLocation + "."

        # If the path length is 1, then the agent is already at the current location
        if (len(path) == 1):
            return "You are already at " + endLocation + "."

        # Find the next step along the path
        nextStep = path[1]
        return "The next location to go to is: " + nextStep 


#
#   Sorting items by quantity
#
class ModuleSortByQuantity(SymbolicModule):

    #
    #   Constructor
    #
    def __init__(self, properties):
        self.moduleName = "sortquantity"
        self.properties = properties

        # A list of observed relevant objects
        self.observedObjects = []


    #
    #   Valid Commands
    #
    def getValidCommands(self):
        out = []        
        
        # Ascending order (least to most)
        out.append("sort ascending")

        # Descending order (most to least)
        out.append("sort descending")

        return out


    #
    #   Run Command
    #
    def runCommand(self, actionStr):
        # Check that this is a valid action
        if (self.isValidCommand(actionStr) == False):
            return "This is not a valid action for this module (" + self.moduleName + ", " + actionStr + ")"

        # Check that we have observed objects with quantities
        if (len(self.observedObjects) == 0):
            return "No objects with quantities have been observed."

        # Interpret the action
        if (actionStr == "sort ascending"):
            objOrder = self.sort()            
            objReferents = [x['referent'] for x in objOrder]
            outStr = "The observed items, sorted in order of increasing quantity, are: " + ", ".join(objReferents) + "."
            return outStr

        elif (actionStr == "sort descending"):
            objOrder = list(reversed(self.sort()))            
            objReferents = [x['referent'] for x in objOrder]
            outStr = "The observed items, sorted in order of decreasing quantity, are: " + ", ".join(objReferents) + "."
            return outStr            


    # Sort the list
    def sort(self):        
        sortedObjects = sorted(self.observedObjects, key=lambda d: d['normalizedQuantity'])
        return sortedObjects


    def sanitizeInputStr(self, inputStr):
        knownUnits = ["mm", "cm", "m", "mg", "g", "kg", "ml", "l"]
        tokens = inputStr.split(" ")

        outTokens = []
        for token in tokens:
            split = re.split('(\d+)',token)
            splitSanitized = [x for x in split if len(x) > 0]            
            outTokens.extend(splitSanitized)

        return " ".join(outTokens)

    # Scrape observation for map related information
    def scrapeFreeLookStr(self, observationStr):
        knownUnits = ["mm", "cm", "m", "mg", "g", "kg", "ml", "l"]

        unitMultipliers = {
            'mm': 1,
            'cm': 10,
            'm': 1000,
            'mg': 1,
            'g': 1000,
            'kg': 1000000,
            'ml': 1,
            'l': 1000,
        }

        # Sanitize observation string in a way that pulls out the known units, making them easier for Spacy's parser to catch.
        observationStr = self.sanitizeInputStr(observationStr)

        # Step 1: Extract quantitied objects (e.g. 5 apples, 50cm of wood)
        doc = nlp(observationStr)
        tokens = [token.text for token in doc]            
        tags = [token.tag_ for token in doc]        

        # Slightly hacky way of simplifying the code block below, to not miss objects that appear at the end of the string. 
        tokens.extend(["", "", "", ""])
        tags.extend(["", "", "", ""])

        print("doc:")
        print(doc)
        print("tokens: " + str(tokens))
        print("tags: " + str(tags))

        # Search for pattern: <num> <object>
        candidates = []        
        for i in range(0, len(tokens)-4):
            if (tags[i] == "CD"):
                quantity = tokens[i]
                if (tags[i+1].startswith("NN")):  
                    found = False
                    if (tags[i+2].startswith("IN")):
                        if (tags[i+3].startswith("NN")):

                            # Check that unit is known                            
                            unit = tokens[i+1].lower()
                            if (unit in knownUnits):
                                # Candidate for something of the form "5kg of apples"
                                normalizedQuantity = float(quantity) * unitMultipliers[unit]
                                referentTokens = tokens[i:i+4]
                                referent = " ".join(referentTokens)

                                packed = {'normalizedQuantity': normalizedQuantity, 'referentTokens:': referentTokens, 'referent': referent} 
                                candidates.append( packed )
                                found = True

                    if (found == False):
                        #print("found: " + str(tokens[i:i+2]))
                        # Candidates for something of the form "5 apples"
                        try:
                            normalizedQuantity = float(quantity)
                            referentTokens = tokens[i:i+2]
                            referent = " ".join(referentTokens)

                            packed = {'normalizedQuantity': normalizedQuantity, 'referentTokens:': referentTokens, 'referent': referent} 
                            candidates.append( packed )

                        except ValueError:
                            pass

        #print("Found candidates: " + str(candidates))

        # TODO: Filter out any low quality candidates?

        # Store
        self.observedObjects = candidates



#
#   Knowledge Base (TWC)
#
class ModuleKnowledgeBaseTWC(SymbolicModule):

    #
    #   Constructor
    #
    def __init__(self, properties):
        self.moduleName = "kb-twc"
        self.properties = properties

        # Load the knowledge base
        self.filename = "kb-twc.tsv"
        self.rows = self.loadTSV(self.filename)


    #
    #   Valid Commands
    #
    def getValidCommands(self):
        out = []        
        actionPrefix = "query " 

        # Queries for the first column (the first element of the triple)
        for row in self.rows:
            firstCol = row[0].strip()
            out.append(actionPrefix + firstCol)            

        # Queries for the last column (the last element of the triple)
        for row in self.rows:
            lastCol = row[2].strip()
            out.append(actionPrefix + lastCol)            

        # Queries for the middle column (the relation)
        for row in self.rows:
            middleCol = row[1].strip()
            out.append(actionPrefix + middleCol)

        # Convert to a set to remove duplicates
        out = list(set(out))

        return out


    #
    #   Run Command
    #
    def runCommand(self, actionStr):
        # Check that this is a valid action
        if (self.isValidCommand(actionStr) == False):
            return "This is not a valid action for this module (" + self.moduleName + ", " + actionStr + ")"

        # Get query results
        queryStr = actionStr[len("query "):]        # Remove the leading 'query ' from the query string
        queryResults = self.runQuery(queryStr)

        # Check that we have a non-zero number of results
        if (len(queryResults) == 0):
            return "No results found."

        # Return the results
        queryResultsStrs = [" ".join(x) for x in queryResults]
        outStr = "The results are:\n " + ".\n ".join(queryResultsStrs)
        return outStr


    # Load the knowledge base
    def loadTSV(self, filename):
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                sanitized = [x.strip() for x in row]
                rows.append(sanitized)
        print ("* Loaded a knowledge base (" + str(filename) + ") with " + str(len(rows)) + " rows.")

        return rows

    # Return any rows, where at least one of the columns matches the queryStr
    def runQuery(self, queryStr):
        resultRows = []
        for row in self.rows:
            include = False
            for col in row:                
                if (col.strip() == queryStr):
                    include = True
                    break
            if (include):
                resultRows.append(row)

        return resultRows


#
#   Tests
#

def testCalc():
    enabledModules = ["calc"]
    properties = {'hidden_num1': '5', 'hidden_num2': '10'}
    moduleInterface = SymbolicModuleInterface(enabledModules, properties)

    validCommands = moduleInterface.getValidCommands()
    print("Valid commands: " + str(validCommands))
    for command in validCommands:
        print("Result of " + str(command) + ": " + str(moduleInterface.runCommand(command)))

def testNavigation():
    enabledModules = ["navigation"]
    properties = {}
    moduleInterface = SymbolicModuleInterface(enabledModules, properties)


def testNavigation1():
    properties = {}
    nav = ModuleNavigation(properties)
    # nav.addEdge("kitchen", "living room")
    # nav.addEdge("kitchen", "hallway")
    # nav.addEdge("kitchen", "pantry")
    # nav.addEdge("kitchen", "backyard")
    # nav.addEdge("hallway", "bathroom")
    # nav.addEdge("living room", "hallway")
    # nav.addEdge("living room", "driveway")

    #nav.scrapeObservationStr("You are in the kitchen. To the north is the living room. To the east is the hallway. To the south is the backyard. To the west is the pantry.")

    nav.scrapeObservationStr("""The map reads:
  The pantry connects to the kitchen.
  The backyard connects to the kitchen, corridor, street and sideyard.
  The alley connects to the driveway and street.
  The sideyard connects to the backyard.
  The garage connects to the driveway.
  The kitchen connects to the backyard, laundry room, living room and pantry.
  The street connects to the supermarket, alley and backyard.
  The bathroom connects to the living room.
  The driveway connects to the alley and garage.
  The supermarket connects to the street.
  The foyer connects to the corridor.
  The laundry room connects to the kitchen.
  The corridor connects to the backyard and foyer.
  The living room connects to the bedroom, bathroom and kitchen.
  The bedroom connects to the living room.
""")

    print( nav.getConnections("kitchen") )

    print( nav.findPath("backyard", "supermarket") )

    print( nav.runCommand("path from living room to pantry") )
    print( nav.runCommand("path from pantry to living room") )
    print( nav.runCommand("path from laundry room to living room") )
    nav.currentLocation = "pantry"
    print( nav.runCommand("path to living room") )
    print( nav.runCommand("path to foyer") )
    print( nav.runCommand("next step to living room") )
    print( nav.runCommand("next step to garage") )


def testSorting():
    enabledModules = ["sortquantity"]
    properties = {}
    moduleInterface = SymbolicModuleInterface(enabledModules, properties)

    #obs = "You are in the kitchen. In one part of the room you see a fridge that is closed. There is also a dining chair that has 15kg of cedar, and 21kg of marble on it. You also see a counter that has 47g of brick, and 25g of oak on it. In another part of the room you see a box, that is empty. In one part of the room you see a dishwasher that is closed. There is also a trash can that is closed. You also see an oven. In another part of the room you see a cutlery drawer that is closed. In one part of the room you see a stove. There is also a kitchen cupboard that is closed."
    #obs = "You are in the supermarket. In one part of the room you see a box, that is empty. There is also a showcase that has 4 watermelons, 30 limes, 44 coconuts, and 8 brocollis on it."
    #obs = "You are in the supermarket. In one part of the room you see a box, that is empty. There is also a showcase that has 27ml of concrete, 48l of acrylic, and 34l of plastic on it. "
    #obs = "You are in the street. In one part of the room you see 41l of plastic. There is also 15ml of steel. You also see 17ml of plastic. In another part of the room you see a box, that is empty."
    #obs = "You are in the kitchen. In one part of the room you see a counter, that has nothing on it. There is also a fridge that is closed. You also see A box, that contains 34ml of concrete, 18ml of plastic, and 29ml of acrylic. In another part of the room you see a dishwasher that is closed. In one part of the room you see a trash can that is closed. There is also an oven. You also see a cutlery drawer that is closed. In another part of the room you see a stove. In one part of the room you see a kitchen cupboard that is closed. There is also a dining chair that has 47l of acrylic, and 35l of concrete on it."
    obs = "You are in the driveway. In one part of the room you see 38l of acrylic. There is also 35l of steel. You also see A box, that contains 11ml of concrete, and 18l of steel. In another part of the room you see 47l of nylon."
    
    inv = ""
    moduleInterface.giveEnvironmentStatus(obs, inv, obs)

    print( moduleInterface.runCommand("sort ascending") )
    print( moduleInterface.runCommand("sort descending") )


def testKBTWC():
    enabledModules = ["kb-twc"]
    properties = {}
    moduleInterface = SymbolicModuleInterface(enabledModules, properties)

    print( moduleInterface.runCommand("query xyzabc"))
    print( moduleInterface.runCommand("query clean blue socks"))


def main():
    #testCalc()

    #testNavigation1()

    testSorting()

    #testKBTWC()


if __name__ == "__main__":
    main()


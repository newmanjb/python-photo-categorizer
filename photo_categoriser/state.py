import utils

"""Represents the current state of the photo categorizer e.g. which photo in the list is currently being displayed and
   what key-folder mappings does the user have.  This class is also responsible for saving and reading the state to and
   from the config file.
"""

class State:

    def fileRemoved(self):
        #Tells the state instance that the current file has been removed
        self.files.pop(self.counter)
        if len(self.files) == 0:
            self.currentFile = None
            self.counter = 0
            self.save()
            return True
        else:
            if (self.counter == len(self.files)):
                self.counter-=1;

            self.currentFile = self.files[self.counter]
            self.save()
            return False

    def incrementCtr(self):
        #Tells the state instance to move along one place in the list of files
        if len(self.files) - 1 == self.counter:
            self.counter = 0
        else :
            self.counter = self.counter + 1

        self.currentFile = self.files[self.counter]
        self.save()

    def decrementCtr(self):
        #Tells the state instance to move back one place in the list of files
        if self.counter == 0:
            self.counter = len(self.files) - 1
        else :
            self.counter = self.counter - 1

        self.currentFile = self.files[self.counter]
        self.save()

    def listMappings(self):
        #List the current key-folder mappings
        mappingsList = []
        for key in self.mappings.keys():
            mappingsList.append(str(key) + "=" + self.mappings[key])
        return mappingsList

    def addMapping(self, value):
        #Add a new mapping for the given folder
        self.mappingKey = self.mappingKey + 1
        self.mappings[self.mappingKey] = value
        toReturn = str(self.mappingKey) + "=" + value
        self.save()
        return toReturn

    def getMappingFor(self, key):
        #Return a string representing the folder that is mapped to the given key
        return self.mappings[key]

    def isAMapping(self, input):
        #Return true if the given string is a key for a mapping
        return input in self.mappings

    def __init__(self,configFile):
        #Read the config file into memory
        self.configFile = configFile

        configMap = {}
        with open(configFile) as cfg:
            for line in cfg:
                key, value = line.split("=")
                configMap[key]=value.rstrip()

        self.sourcePath=configMap["sourcePath"]
        self.destPath=configMap["destPath"]

        files = utils.getFiles(self.sourcePath, ".JPG")
        files.extend(utils.getFiles(self.sourcePath, ".jpg"))
        if(len(files) == 0):
            print("NO FILES FOUND IN " + self.sourcePath + "  EXITING ...")
            exit(0);
        self.files = sorted(files);

        if "counter" in configMap :
            self.counter=int(configMap["counter"])
        else :
            self.counter = 0

        self.mappings={}
        if "1" in configMap:
            self.mappingKey=int(configMap["mappingKey"])
            for n in range(1, self.mappingKey + 1):
                self.mappings[n]=configMap[str(n)]
        else:
            self.mappingKey = 0

        if "currentFile" in configMap:
            self.currentFile = configMap["currentFile"]
        else:
            self.currentFile = self.files[self.counter]

        #Now that we have set up the initial state we should save it, mainly so as the photo-viewer can read
        #what the current file now is
        self.save()

    def save(self):
        #Write the current state to the config file
        configMap = {}
        configMap["sourcePath"] = self.sourcePath
        configMap["destPath"] = self.destPath
        configMap["counter"] = str(self.counter)
        configMap["mappingKey"] = str(self.mappingKey)
        configMap["currentFile"] = self.currentFile
        for key in self.mappings.keys():
            configMap[str(key)]=str(self.mappings[key])

        fileNamesString = []
        for fileName in self.files:
            fileNamesString.append(fileName)
        configMap["files"]=",".join(fileNamesString)

        if self.currentFile == None:
            configMap["currentFile"] = "None"

        with open(self.configFile, "w") as file:
            for key in configMap.keys():
                line = key + "=" + configMap[key] + "\n"
                file.write(line)

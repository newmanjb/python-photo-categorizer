from os import listdir, remove, mkdir, rename
from os.path import isfile, join

"""Utility functions for the photo categorizer
"""

def getFiles(dirPath,suffix):
    #Return a list of files from the given directory that have the given suffix
    onlyFiles = [f for f in listdir(dirPath) if isfile(join(dirPath, f)) and f.endswith(suffix)]
    return onlyFiles

def removefile(basepath, name):
    remove(join(basepath, name))

def makeDir(basepath, name):
    newDir = join(basepath, name)
    mkdir(newDir);
    return newDir

def moveFile(sourcePath, name, destDirPath):
    rename(join(sourcePath, name), join(destDirPath, name))
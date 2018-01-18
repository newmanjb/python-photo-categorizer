from os import listdir, remove, mkdir, rename
from os.path import join
from PIL import Image

"""Utility functions for the photo categorizer
"""

def getFiles(dirPath,suffix):
    """Return a list of tuples with the structure ("file from the given directory that has the given suffix", "date of creation")"""
    onlyFiles = [f for f in getFileTuples(dirPath) if f[0].endswith(suffix)]
    return onlyFiles

def removefile(basepath, name):
    remove(join(basepath, name))

def makeDir(basepath, name):
    newDir = join(basepath, name)
    mkdir(newDir);
    return newDir

def moveFile(sourcePath, name, destDirPath):
    rename(join(sourcePath, name), join(destDirPath, name))

def getFileTuples(dirPath) :
    files = listdir(dirPath)
    validFiles = []
    dates = []
    for file in files:
        try:
            image = Image.open(join(dirPath, file));
            exif = image._getexif()
            date = "No creation date found"
            if 36867 in exif:
                date = exif[36867]

            validFiles.append(file)
            dates.append(date)
        except:
            pass

    return zip(validFiles, dates)

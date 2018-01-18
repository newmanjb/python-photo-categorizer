import string;
import sys;

from photo_categoriser import state;

from utils.file_handling import file_utils

COMMAND_FORWARD = "f"
COMMAND_BACK = "b"
COMMAND_DEL = "d"
COMMAND_MAKE = "make"
COMMAND_EXIT = "exit"
COMMAND_PUT = "put"
COMMAND_LIST = "l"
COMMAND_HELP = "help"

"""Main file for the photo categorizer.  This application allows users to quickly examine and categorize images e.g.
   photos, from a given source.  It is particularly useful for large amounts of photos from a smart-phone that were
   taken over a long period of time and which the user wishes to sort and back-up!  The application is command-line based.
   This file takes input from the user and contains the implementation for the various operations they are able to perform.
   This should be run with a single argument, which is the full path to the config file.  The config file should
   contain a source path and a destination path as in the example below:

   sourcePath=C:/photos
   destPath=C:/holiday_photos/parsedPhotos

   The source will be where the images to be categorized are taken from and the destination is where they will be
   copied to.

   The application will obtain a list of the images from the source directory and allow the user to navigate
   through the list, displaying each one.  The user is able to specify folder names for the photos, where a folder
   with the equivalient name will be created in the destination directory.  The user will be given a unique "key" for
   that folder name, which will just be an integer.  From then on they will be able to move the currently displayed
   photo to that folder from the source directory just by typing that key e.g. '3'.  Photos can also be deleted.

   A full list of the commands can be obtained at any time by typing 'help'.

   Also, the application saves its state,
   meaning that if a user exits and then restarts at a later time all their key-folder mappings will still be present
   and the displayed image will be whatever was being displayed when they shut the application down.

   This application should be run with an appropriate "photo viewer" application that displays the current photo.
   This application saves the currently viewed file to its config, so all the photo viewer application needs to do
   is poll this config file for the "currentFile" property from the config and append that to the "sourcePath" property
   from the config.  It will then have the image file to display.
   I have supplied a basic default photo viewer, written in java swing, with this application.

   When there are no more images left to categorize the user will be informed.  If the user wants to process a new set
   of photos they should delete all the config from the config file apart from the source and destination directories,
   before starting the application again.
"""


def isANumber(input):
    try :
        int(input)
        return True
    except ValueError :
        return False

def doDel(state) :
    """remove a file"""
    fileToRemove = state.currentFile[0]
    file_utils.removefile(state.sourcePath, fileToRemove)
    if(state.fileRemoved() == False) :
        print("Removed: " + fileToRemove)
        printCurrentFile(state.currentFile)
    else :
        print("ALL FILES PROCESSED.  PLEASE CHECK THE FOLLOWING NEW DIRS IF ANY:  EXITING..")
        doListMappings(state)
        exit(0)



def doMove(state, userInput) :
    """move the current file to the folder specified by the key that the user has given"""
    fileToMove = state.currentFile[0]
    destDir = state.getMappingFor(userInput)
    file_utils.moveFile(state.sourcePath, fileToMove, destDir)
    if(state.fileRemoved() == False):
        print("Moved: " + fileToMove + " to " + destDir)
        printCurrentFile(state.currentFile)
    else:
        print("ALL FILES PROCESSED.  PLEASE CHECK THE FOLLOWING NEW DIRS:  EXITING..")
        doListMappings(state)
        exit(0)

def doForward(state) :
    """move forward in the list"""
    state.incrementCtr()
    printCurrentFile(state.currentFile)

def doBack(state) :
    """move backward in the list"""
    state.decrementCtr()
    printCurrentFile(state.currentFile)

def doMake(state, dirName):
    """Create a folder and a key for it"""
    print("New mapping: " + state.addMapping(file_utils.makeDir(state.destPath, dirName)))
    printCurrentFile(state.currentFile)

def doListMappings(state):
    """Print a list of current mappings e.g. 1=C:/photos/Summer_Of_69, where 1 will be the key"""
    print("\n".join(state.listMappings()));
    printCurrentFile(state.currentFile)

def doHelp(state):
    """Print the commands and what they do"""
    print("\n".join(["'f' - forward", "'b' - back", "'d' - delete", "'your new folder name' - create a key-folder mapping e.g. 'Holiday_August_2016'",
                     "'your mapping key' - move to folder under that key e.g. '2'", "'exit' - Quit", "'l' - list mappings", "'help' - list commands"]))
    printCurrentFile(state.currentFile)

def format_filename(s):
    """Remove invalid characters from a proposed folder name"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

def printCurrentFile(currentFile):
    print("Current File: ", currentFile[0], ", Date Created: ", currentFile[1])


if __name__ == "__main__":

    #Get the config file and build a state instance from it
    state = state.state(sys.argv[1])

    #Build a dictionary of commands e.g. 'f', 'b', mapped to their appropriate functions
    actions = {}
    actions[COMMAND_DEL] = doDel
    actions[COMMAND_FORWARD] = doForward
    actions[COMMAND_BACK] = doBack
    actions[COMMAND_MAKE] = doMake
    actions[COMMAND_PUT] = doMove
    actions[COMMAND_LIST] = doListMappings
    actions[COMMAND_HELP] = doHelp

    printCurrentFile(state.currentFile)

    #Prompt for input from the user until they exit
    userInput = ""
    while(userInput != COMMAND_EXIT):
        userInput = input()

        if userInput in actions :
            actions[userInput](state)

        elif(isANumber(userInput) and state.isAMapping(int(userInput))) :
            actions[COMMAND_PUT](state, int(userInput))
        elif userInput != COMMAND_EXIT :
            dirName = format_filename(userInput)
            confirm = input("Make dir '" + userInput + "' ?  y/n")
            if(confirm == "y"):
                actions[COMMAND_MAKE](state, dirName)
            else :
                print("Not making dir")
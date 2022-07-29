import os


def getMainDirectory():
    return os.getcwd()


def isFolderExist(folderName):
    return os.path.isdir(folderName)


def createFolder(folderName):
    os.mkdir(folderName)


def cdToFolder(folderName):
    os.chdir(folderName)


def is_FistAndBall_ScoreLogFile_Exist():
    scoreLogFileName = "Score-Log-Fist&Ball.txt"
    return os.path.isfile(scoreLogFileName)


def createLogFile_FistAndBall():
    scoreLogFileName = "Score-Log-Fist&Ball.txt"
    file = open(scoreLogFileName, "x")
    file.write(
        "| "
        + "Day Month  Hour     Year  "
        + "|"
        + "  Difficulty  "
        + "|"
        + "  Total Time  "
        + "|"
        + "  Capture Time  "
        + "|"
        + "  Score  "
        + "|"
        + "  Status      "
        + "|\n"
    )  # don't touch this :)
    file.close()

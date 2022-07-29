import numpy as np
import scipy
import bpy


def fistAndBall_logScore_SaveData(
    date, difficulty, totalTime, capturedTime, status, sampledData, sampleIndex
):
    scoreLogFileName = "Score-Log-Fist&Ball.txt"
    score = logScore(
        scoreLogFileName, date, difficulty, totalTime, capturedTime, status
    )
    fileName = logFileName("Fist&Ball", difficulty, date)
    saveSamples(fileName, sampledData, sampleIndex)

    return score


def saveSamples(fileName, sampledData, sampleIndex):
    scipy.io.savemat(
        fileName,
        {
            "data": np.array(
                list({key: sampledData[key] for key in range(0, sampleIndex)}.items()),
                dtype=object,
            )
        },
        do_compression=True,
    )


def logScore(scoreLogFileName, date, difficulty, totalTime, capturedTime, status):

    score = (capturedTime / totalTime) * 100
    # message = "{date} ==> Difficulty : {difficulty} , Total Time : {totalTime:.2f} , Capture Time : {capturedTime:.2f} , Score : {score:.2f}\n".format(date =date,difficulty=difficulty,totalTime=totalTime,capturedTime=capturedTime,score = score)
    message = (
        "| "
        + "{date}".format(date=date)
        + " " * (26 - len(date))
        + "|  "
        + "{difficulty}".format(difficulty=difficulty)
        + " " * (12 - len(difficulty))
        + "|  "
        + "{totalTime:.2f}".format(totalTime=totalTime)
        + " " * (12 - len(str("{totalTime:.2f}".format(totalTime=totalTime))))
        + "|  "
        + "{capturedTime:.2f}".format(capturedTime=capturedTime)
        + " " * (14 - len(str("{capturedTime:.2f}".format(capturedTime=capturedTime))))
        + "|  "
        + "{score:.2f}".format(score=score)
        + " " * (7 - len(str("{score:.2f}".format(score=score))))
        + "|  "
        + "{status}".format(status=status)
        + " " * (12 - len(status))
        + "|\n"
    )

    with open(scoreLogFileName, "a") as file:

        file.write(message)
    return score


def logFileName(fName, difficulty, date):
    fileName = fName + "," + str(date) + "," + str(difficulty) + ".mat"
    unWantedChar = ":"
    for char in unWantedChar:
        fileName = fileName.replace(char, "")

    return fileName


def showMessageBox(obj, context, message="", title="Score Box", icon="INFO"):
    def draw(obj, context):
        obj.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

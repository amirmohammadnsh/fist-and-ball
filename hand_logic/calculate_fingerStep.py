def calculateFingerStep(magnitude, magnet, selectedSensor):
    fingerStep = 0

    for i in range(0, 9):
        if (
            magnitude[0, selectedSensor - 1] / magnet.maxThreshold
        ) * 100 <= magnet.scaleOfValue[i]:
            fingerStep = i
            break
        elif (
            magnitude[0, selectedSensor - 1] / magnet.maxThreshold
        ) * 100 > magnet.scaleOfValue[8]:
            fingerStep = 9
            break
    return fingerStep

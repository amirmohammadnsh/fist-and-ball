class ImplantedMagnet:
    maxThreshold = 0
    scaleOfValue = [None] * 9
    tagOne = {
        "maxThreshold": 2000,
        "scaleOfValue": [60, 63, 68, 72, 76, 80, 81, 83, 85],
    }
    tagTwo = {
        "maxThreshold": 10000,
        "scaleOfValue": [70, 73, 76, 79, 82, 85, 88, 91, 95],
    }
    tagThree = {
        "maxThreshold": 4500,
        "scaleOfValue": [87, 88, 89, 90, 91, 92, 93, 94, 95],
    }

    def __init__(self, tagName):
        if tagName == "tagOne":
            self.maxThreshold = self.tagOne["maxThreshold"]
            self.scaleOfValue = self.tagOne["scaleOfValue"]
        elif tagName == "tagTwo":
            self.maxThreshold = self.tagTwo["maxThreshold"]
            self.scaleOfValue = self.tagTwo["scaleOfValue"]
        elif tagName == "tagThree":
            self.maxThreshold = self.tagThree["maxThreshold"]
            self.scaleOfValue = self.tagThree["scaleOfValue"]

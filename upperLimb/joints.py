from upperLimb.limbProperties import UpperLimbProp


class ThumbFinger:
    name = "thmb"
    numberOfLinks = UpperLimbProp.thumbLinks.value
    # maxDegreeLimit = 80
    # minDegreeLimmit = 0
    bnsNames = [None] * numberOfLinks

    def __init__(self):

        self.initBoneNames(self.bnsNames, self.name, self.numberOfLinks)

    def initBoneNames(self, listBnsNames, fingerName, numberLinksFingers):

        for i in range(numberLinksFingers):
            listBnsNames[i] = fingerName + str(i)


class PinkyFinger:
    name = "pinky"
    numberOfLinks = UpperLimbProp.pinkyLinks.value
    # maxDegreeLimit = 100
    # minDegreeLimmit = 0
    bnsNames = [None] * numberOfLinks

    def __init__(self):

        self.initBoneNames(self.bnsNames, self.name, self.numberOfLinks)

    def initBoneNames(self, listBnsNames, fingerName, numberLinksFingers):

        for i in range(numberLinksFingers):
            listBnsNames[i] = fingerName + str(i)


class RingFinger:
    name = "ring"
    numberOfLinks = UpperLimbProp.ringLinks.value
    # maxDegreeLimit = 100
    # minDegreeLimmit = 0
    bnsNames = [None] * numberOfLinks

    def __init__(self):

        self.initBoneNames(self.bnsNames, self.name, self.numberOfLinks)

    def initBoneNames(self, listBnsNames, fingerName, numberLinksFingers):

        for i in range(numberLinksFingers):
            listBnsNames[i] = fingerName + str(i)


class MidFinger:
    name = "mid"
    numberOfLinks = UpperLimbProp.middleLinks.value
    # maxDegreeLimit = 100
    # minDegreeLimmit = 0
    bnsNames = [None] * numberOfLinks

    def __init__(self):

        self.initBoneNames(self.bnsNames, self.name, self.numberOfLinks)

    def initBoneNames(self, listBnsNames, fingerName, numberLinksFingers):

        for i in range(numberLinksFingers):
            listBnsNames[i] = fingerName + str(i)


class IndexFinger:
    name = "index"
    numberOfLinks = UpperLimbProp.indexLinks.value
    # maxDegreeLimit = 100
    # minDegreeLimmit = 0
    bnsNames = [None] * numberOfLinks

    def __init__(self):

        self.initBoneNames(self.bnsNames, self.name, self.numberOfLinks)

    def initBoneNames(self, listBnsNames, fingerName, numberLinksFingers):

        for i in range(numberLinksFingers):
            listBnsNames[i] = fingerName + str(i)


class ForeArm:
    name = "foreArm"
    numberOfLinks = UpperLimbProp.foreArmLinks.value
    bnsNames = [None] * numberOfLinks

    def __init__(self):

        self.initBoneNames(self.bnsNames, self.name, self.numberOfLinks)

    def initBoneNames(self, listBnsNames, fingerName, numberLinksFingers):

        for i in range(numberLinksFingers):
            listBnsNames[i] = fingerName + str(i)

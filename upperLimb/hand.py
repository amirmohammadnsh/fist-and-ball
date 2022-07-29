from upperLimb.limbProperties import UpperLimbProp
from upperLimb.skeleton import Skeleton
import math
import bpy
from bpy.props import IntProperty


class VirtualHand:
    skeleton = None
    handArmature = None
    pinkyBones = [None] * UpperLimbProp.pinkyLinks.value
    indexBones = [None] * UpperLimbProp.indexLinks.value
    middleBones = [None] * UpperLimbProp.middleLinks.value
    ringBones = [None] * UpperLimbProp.ringLinks.value
    thumbBones = [None] * UpperLimbProp.thumbLinks.value
    foreArmBones = [None] * UpperLimbProp.foreArmLinks.value

    thumbDOF = 65
    pinkyDOF = 95
    ringDOF = 90
    middleDOF = 90
    indexDOF = 90
    foreArmDOFUp = 30
    foreArmDOFDown = 40
    # thumbDOF: IntProperty(name="thumbDOF", default=65)
    # pinkyDOF: IntProperty(name="pinkyDOF", default=95)
    # ringDOF: IntProperty(name="ringDOF", default=90)
    # middleDOF: IntProperty(name="middleDOF", default=90)
    # indexDOF: IntProperty(name="indexDOF", default=90)
    # foreArmDOFUp: IntProperty(name="foreArmDOFUp", default=30)
    # foreArmDOFDown: IntProperty(name="foreArmDOFDown", default=40)

    def __init__(self):
        self.skeleton = Skeleton()
        self.handArmature = bpy.data.objects["Armature"]
        self.initFingerBones()

    def initFingerBones(self):
        for i in range(UpperLimbProp.pinkyLinks.value):
            self.pinkyBones[i] = self.handArmature.pose.bones[
                self.skeleton.pinky.bnsNames[i]
            ]
            self.initDegreeBones(self.pinkyBones[i])

        for i in range(UpperLimbProp.indexLinks.value):
            self.indexBones[i] = self.handArmature.pose.bones[
                self.skeleton.index.bnsNames[i]
            ]
            self.initDegreeBones(self.indexBones[i])

        for i in range(UpperLimbProp.ringLinks.value):
            self.ringBones[i] = self.handArmature.pose.bones[
                self.skeleton.ring.bnsNames[i]
            ]
            self.initDegreeBones(self.ringBones[i])

        for i in range(UpperLimbProp.middleLinks.value):
            self.middleBones[i] = self.handArmature.pose.bones[
                self.skeleton.middle.bnsNames[i]
            ]
            self.initDegreeBones(self.middleBones[i])

        for i in range(UpperLimbProp.thumbLinks.value):
            self.thumbBones[i] = self.handArmature.pose.bones[
                self.skeleton.thumb.bnsNames[i]
            ]
            self.initDegreeBones(self.thumbBones[i])

        for i in range(UpperLimbProp.foreArmLinks.value):
            self.foreArmBones[i] = self.handArmature.pose.bones[
                self.skeleton.foreArm.bnsNames[i]
            ]
            self.initDegreeBones(self.foreArmBones[i])

    def initDegreeBones(self, bone):
        bone.rotation_mode = "XYZ"
        bone.rotation_euler = [math.radians(0), math.radians(0), math.radians(0)]

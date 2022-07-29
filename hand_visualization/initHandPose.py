
import math

def initPose(hand,gesture):
    if gesture =="fist":
        hand.thumbBones[0].rotation_euler = [
            math.radians(0),
            math.radians(0),
            math.radians(-13),
        ]

import math


def showGesture_based_on_fingerStep(hand, gesture, fingerStep):

    if gesture == "fist":
        hand.thumbBones[0].rotation_euler[0] = math.radians(
            hand.thumbDOF - (hand.thumbDOF / 9) * fingerStep
        )

        hand.pinkyBones[0].rotation_euler[0] = math.radians(
            hand.pinkyDOF - (hand.pinkyDOF / 9) * fingerStep
        )
        hand.ringBones[0].rotation_euler[0] = math.radians(
            hand.ringDOF - (hand.ringDOF / 9) * fingerStep
        )
        hand.middleBones[0].rotation_euler[0] = math.radians(
            hand.middleDOF - (hand.middleDOF / 9) * fingerStep
        )
        hand.indexBones[0].rotation_euler[0] = math.radians(
            hand.indexDOF - (hand.indexDOF / 9) * fingerStep
        )

from upperLimb.joints import (
    ThumbFinger,
    PinkyFinger,
    RingFinger,
    MidFinger,
    IndexFinger,
    ForeArm,
)


class Skeleton:
    thumb = None
    pinky = None
    ring = None
    middle = None
    index = None
    foreArm = None

    def __init__(self):

        self.thumb = ThumbFinger()
        self.pinky = PinkyFinger()
        self.ring = RingFinger()
        self.middle = MidFinger()
        self.index = IndexFinger()
        self.foreArm = ForeArm()

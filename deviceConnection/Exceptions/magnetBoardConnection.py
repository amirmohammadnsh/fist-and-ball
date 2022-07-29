class MagnetBoardSetupConnectionFailed(Exception):
    def __init__(self) -> None:
        super().__init__("Cannot setup device Connection")

class MagnetBoardStartConnectionFailed(Exception):
    def __init__(self) -> None:
        super().__init__("Cannot Start device Connection")


class MagnetBoardConnectionLost(Exception):
    def __init__(self) -> None:
        super().__init__("Device Connection Has Been Lost!")

class MagnetBoardStopConnectionFailed(Exception):
    def __init__(self) -> None:
        super().__init__("Device Connection Has Already Been Closed!")

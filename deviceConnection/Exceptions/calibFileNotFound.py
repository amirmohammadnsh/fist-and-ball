class CalibrationFileNotFound(Exception):
    def __init__(self) -> None:
        super().__init__("Calibration Params File Has Not Been Found")

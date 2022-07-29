import socket
import threading
from operator import itemgetter
import numpy as np
from scipy.io import loadmat
from deviceConnection.Exceptions import magnetBoardConnection, calibFileNotFound
import os


class GadgetConnection(threading.Thread):

    running = False
    port = 0
    ip = ""
    connection = []
    errorMsg = ""
    interrupted = False
    finished = False

    magnitude = 0
    selectedSensor = 0
    numberOfSensors = 0
    lenOfData = 0
    recvData = 0
    dataByte = 0
    checkedIndices = 0
    sampleRecvProper = False

    mainDirectory = ""
    calibPath = ""
    senOffset = 0
    senGain = 0
    senRotation = 0
    refr = 496.5

    def __init__(
        self,
        nSensors,
        devicePort,
        deviceIP,
        doCalibData=False,
        calibPath="",
    ):

        threading.Thread.__init__(self)
        self.numberOfSensors = nSensors  # number of sensors on the device
        self.lenOfData = (self.numberOfSensors * 4) * 2 + 2
        self.recvData = [0] * (self.lenOfData // 2 - 1)
        self.dataByte = bytes(self.lenOfData)
        self.checkedIndices = [i * 4 for i in (list(range(0, self.numberOfSensors)))]

        self.magnitude = np.zeros((1, self.numberOfSensors))
        self.doCalibData = doCalibData
        self.ip = deviceIP
        self.port = devicePort

        if doCalibData:

            self.senOffset = np.zeros((self.numberOfSensors, 3))
            self.senGain = np.zeros((self.numberOfSensors, 3))
            self.senRotation = np.zeros((self.numberOfSensors, 9))
            self.magnitude = np.zeros((1, self.numberOfSensors))
            self.calibPath = calibPath

            self.mainDirectory = os.getcwd()
            os.chdir(self.calibPath)
            try:
                self.senOffset = np.array(loadmat("senORG.mat")["offset"])
                self.senGain = np.array(loadmat("senORG.mat")["gain"])
                self.senRotation = np.array(loadmat("senORG.mat")["rotation"])
                os.chdir(self.mainDirectory)

            except Exception as error:
                os.chdir(self.mainDirectory)
                print(error)
                raise calibFileNotFound.CalibrationFileNotFound

        try:
            self.connection = self.setupConnection()
        except magnetBoardConnection.MagnetBoardSetupConnectionFailed as error:
            print(error)
            raise magnetBoardConnection.MagnetBoardSetupConnectionFailed

    def start(self):
        print("Starting Device Connection ")
        try:
            self.connection.connect((self.ip, self.port))
            self.running = True
            threading.Thread.start(self)

        except Exception as error:
            self.errorMsg = error
            raise magnetBoardConnection.MagnetBoardStartConnectionFailed

    def stop(self):
        print("Stopping Device Connection ")
        self.running = False
        try:
            self.connection.close()
        except Exception as error:
            print(error)
            raise magnetBoardConnection.MagnetBoardStopConnectionFailed

    def setupConnection(self):
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.settimeout(1)
            connection.setblocking(True)
            connection.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 100, 100))
            return connection
        except Exception as error:
            print(error)
            raise magnetBoardConnection.MagnetBoardSetupConnectionFailed

    def run(self):

        while self.running:

            try:

                self.dataByte = self.connection.recv(self.lenOfData)
                self.sampleRecvProper, self.recvData = self.isDataCorrect()

            except Exception as error:
                if self.interrupted == False and self.finished == False:
                    self.sampleRecvProper = False
                    self.recvData = []
                    self.running = False
                    print(error)
                    print("Device Connection Lost Or Recieved Data is Anormal")
                    self.errorMsg = "Connection Lost"

    def isDataCorrect(self):

        if len(self.dataByte) != self.lenOfData:
            return False, [0] * (self.lenOfData // 2 - 1)
        if (
            self.dataByte[self.lenOfData - 2] | self.dataByte[self.lenOfData - 1] << 8
        ) != 32767:
            # print("Terminator Not Reached")
            return False, [0] * (self.lenOfData // 2 - 1)
        i = 0
        for index in range(0, (self.lenOfData // 2 - 1)):
            self.recvData[index] = self.convertToInt(
                self.dataByte[i], self.dataByte[i + 1]
            )
            i = i + 2
        if list(itemgetter(*self.checkedIndices)(self.recvData)) != list(
            range(1, self.numberOfSensors + 1)
        ):
            # print("Sensors are not Sorted")
            return False, [0] * (self.lenOfData // 2 - 1)
        return True, self.recvData

    def convertToInt(self, firstVal, secVal):
        result = firstVal | secVal << 8
        if result > 32767:
            result -= 65536
        return result

    def calculateMagnitude(self):
        if self.doCalibData:
            vals = np.zeros((1, 3))

            for i in range(self.numberOfSensors):
                vals[0:3] = (
                    self.recvData[(i + 1) * 4 - 3 : (i + 1) * 4]
                    - self.senOffset[i, 0:3]
                )
                vals[0:3] = vals[0:3].dot(
                    self.senRotation[i, 0:9].reshape(3, 3, order="F")
                )
                self.magnitude[0, i] = np.sqrt(
                    np.power(vals[0, 0] / self.senGain[i, 0] * self.refr, 2)
                    + np.power(vals[0, 1] / self.senGain[i, 1] * self.refr, 2)
                    + np.power(vals[0, 2] / self.senGain[i, 2] * self.refr, 2)
                )

        elif not self.doCalibData:
            for i in range(self.numberOfSensors):
                vals[0:3] = (
                    self.recvData[(i + 1) * 4 - 3 : (i + 1) * 4]
                    - self.senOffset[i, 0:3]
                )
                self.magnitude[0, i] = np.sqrt(
                    np.power(vals[0, 0], 2)
                    + np.power(vals[0, 1], 2)
                    + np.power(vals[0, 2], 2)
                )

        return self.magnitude

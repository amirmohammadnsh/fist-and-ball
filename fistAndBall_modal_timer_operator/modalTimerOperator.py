import time
import bpy
from bpy.props import IntProperty, StringProperty, FloatProperty
from upperLimb.hand import VirtualHand
from hand_visualization.gestureviz import showGesture_based_on_fingerStep
from hand_visualization.initHandPose import initPose
from hand_logic.calculate_fingerStep import calculateFingerStep
from implantedMagnets.implantsProp import ImplantedMagnet
from deviceConnection.magnetometerBoard import GadgetConnection
from sceneObjects.placeOrangeBall import createAndPlaceBall
from sceneObjects.operations import *
from leds.nineLeds import createAndPlace9Leds, updateLeds
from sampleLogger.directoryManager import *
from sampleLogger.logger import fistAndBall_logScore_SaveData, showMessageBox


class ModalTimerOperatorFistBall(bpy.types.Operator):

    bl_idname = "wm.modal_timer_operator_1"  # _1 is dedicated to FistAndBall_Add-On
    bl_label = "Modal Timer Operator - Exercise on Fist"

    selectedSensor = 2  # monitor sensor data to perform hand gesture
    nSensors = 16
    devicePort = 23
    deviceIp = "192.168.4.1"
    doCalibData = True
    calibPath = (
        "E:/blender-fum-virtual-hand/fum-virtual-hand-env/Fist&Ball/calibrationParams"
    )

    timer = None
    gadgetConnection = None

    difficulty: StringProperty(name="difficulty", default="Simple")

    gameDuration: FloatProperty(name="gameDuration", default=120.0)

    sampleIndex = 0
    date = ""
    sampledData = {}
    data = [0] * (nSensors * 4)
    refreshRate = 0.001

    gestureTypes = 0
    selectedGesture: IntProperty(name="selectedGesture", default=0)
    gestureName = 0
    tags = 0
    selectedTag: IntProperty(name="selectedTag", default=0)
    tagName = ""
    magnet = []

    fingerStep = 0
    currentFingerStep = 0
    prevFingerStep = 0
    hand = None

    beginBallPosition = 0.85000
    endBallPosition = 0.24000
    currentBallPosition = 0.00000
    ballSpeed = 0.00000
    ballOffset = 0.00000

    downMove = False
    upMove = False
    busyHand = False

    startTime = 0
    elapsedTime = 0
    captureBallFirstTime = True
    captureBallStartSec = 0.00000
    capturedBallSec = 0.000
    score = 0
    dirLocation = "Fist&Ball-Log-Files"
    mainDirectory = ""

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        context.scene.panelAccess_FistAndBall = False  ### Disabling the ui_panel
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
        ### Check for availibility of the orange ball in the scene
        createAndPlaceBall(self.beginBallPosition)
        self.downMove = True
        self.currentBallPosition = self.beginBallPosition

        ### setting game mode properties
        if self.difficulty == "easy":
            self.ballSpeed = 0.00500
            self.ballOffset = 0.01000
        elif self.difficulty == "medium":
            self.ballSpeed = 0.00800
            self.ballOffset = 0.01000
        elif self.difficulty == "hard":
            self.ballSpeed = 0.02000
            self.ballOffset = 0.01000
        print(self.difficulty)

        ### Initializing LED objects in the scene
        createAndPlace9Leds()

        ### Initialization of Gesture names and Tags
        self.gestureTypes = ["fist", "thumb", "wristUp", "wristDown"]  # 0 , 1 , 2 , 3
        # self.selectedGesture will be chosen from  0 , 1 , 2 , 3
        self.gestureName = self.gestureTypes[self.selectedGesture]
        print(self.gestureName)

        self.tags = ["tagOne", "tagTwo", "tagThree"]
        # self.selectedTag will be chosen from  0 , 1 , 2
        self.tagName = self.tags[self.selectedTag]
        print(self.tagName)
        self.magnet = ImplantedMagnet(self.tagName)

        self.date = time.asctime(time.localtime(time.time()))
        print(self.date)
        print(self.gameDuration)
        ### call virtual hand by its name in the scene and set its mode to "pose"
        bpy.context.view_layer.objects.active = bpy.data.objects["Armature"]
        bpy.ops.object.mode_set(mode="POSE")
        bpy.context.object.show_in_front = False
        ### initialize hand
        self.hand = VirtualHand()
        self.currentFingerStep = 9
        initPose(self.hand, self.gestureName)
        ### end of hand initialization

        self.mainDirectory = getMainDirectory()

        if not isFolderExist(self.dirLocation):
            createFolder(self.dirLocation)

        cdToFolder(self.dirLocation)

        if not is_FistAndBall_ScoreLogFile_Exist():
            createLogFile_FistAndBall()
        ### set args for GadgetConnection
        try:
            self.gadgetConnection = GadgetConnection(
                self.nSensors,
                self.devicePort,
                self.deviceIp,
                self.doCalibData,
                self.calibPath,
            )

        except Exception as error:
            self.report({"ERROR"}, str(error))
            context.scene.panelAccess_FistAndBall = True
            cdToFolder(self.mainDirectory)
            return {"CANCELLED"}

        try:
            self.gadgetConnection.start()
            self.report({"INFO"}, " Connected Successfully ")
            wm = context.window_manager
            self.timer = wm.event_timer_add(self.refreshRate, window=context.window)
            wm.modal_handler_add(self)
            self.startTime = time.time()
            return {"RUNNING_MODAL"}
        except Exception as error:
            self.gadgetConnection.stop()
            self.report({"ERROR"}, str(error))
            context.scene.panelAccess_FistAndBall = True
            cdToFolder(self.mainDirectory)
            return {"CANCELLED"}

    def modal(self, context, event):

        if event.type in {"ESC"}:
            self.elapsedTime = time.time() - self.startTime
            self.gadgetConnection.interrupted = True
            self.gadgetConnection.stop()
            updateLeds(0)
            self.score = fistAndBall_logScore_SaveData(
                self.date,
                self.difficulty,
                self.elapsedTime,
                self.capturedBallSec,
                "Interrupted",
                self.sampledData,
                self.sampleIndex,
            )

            self.cancel(context)
            self.report(
                {"INFO"},
                " Stopped By User,  {score:.2f} /100  ".format(score=self.score),
            )
            showMessageBox(
                self,
                context,
                message=" Your Score is {score:.2f} ".format(score=self.score),
            )
            context.scene.panelAccess_FistAndBall = True
            cdToFolder(self.mainDirectory)
            return {"CANCELLED"}

        if event.type == "TIMER":

            # start downward mvement of ball
            if self.downMove == True and self.busyHand == False:
                if (
                    self.currentBallPosition > self.endBallPosition
                    and self.currentFingerStep >= 6
                ):
                    self.currentBallPosition -= self.ballSpeed
                    changeLocation(
                        bpy.data.objects["Sphere"], "z", self.currentBallPosition
                    )
                elif self.currentBallPosition > self.endBallPosition + 0.20000:
                    self.currentBallPosition -= self.ballSpeed
                    changeLocation(
                        bpy.data.objects["Sphere"], "z", self.currentBallPosition
                    )
                else:

                    self.downMove = False
                    self.upMove = True
            # start upward movement of ball
            elif self.upMove == True and self.busyHand == False:

                if self.currentBallPosition < self.beginBallPosition:

                    self.currentBallPosition += self.ballSpeed
                    changeLocation(
                        bpy.data.objects["Sphere"], "z", self.currentBallPosition
                    )
                else:
                    self.downMove = True
                    self.upMove = False

            if self.gadgetConnection.sampleRecvProper == True:

                self.data = self.gadgetConnection.recvData
                # check if finger moved
                self.magnitude = self.gadgetConnection.calculateMagnitude()
                self.fingerStep = calculateFingerStep(
                    self.magnitude, self.magnet, self.selectedSensor
                )
                if self.currentFingerStep != self.fingerStep:
                    self.currentFingerStep = self.fingerStep
                    showGesture_based_on_fingerStep(
                        self.hand, self.gestureName, self.currentFingerStep
                    )
                    updateLeds(self.currentFingerStep)

                    if (
                        self.currentBallPosition > 0.30000
                        and self.currentBallPosition < 0.30000 + self.ballOffset
                    ) and self.currentFingerStep == 6:
                        # print("firs",self.endBallPosition,self.currentBallPosition,self.endBallPosition+self.ballOffset,self.currentFingerStep)
                        self.busyHand = True
                        self.prevFingerStep = self.currentFingerStep
                    elif (
                        self.currentBallPosition > self.endBallPosition
                        and self.currentBallPosition < 0.25000 + self.ballOffset
                    ) and self.currentFingerStep == 7:
                        # print("second",self.endBallPosition,self.currentBallPosition,self.endBallPosition+self.ballOffset,self.currentFingerStep)
                        self.busyHand = True
                        self.prevFingerStep = self.currentFingerStep
                    elif (
                        self.currentFingerStep == 7
                        and self.prevFingerStep == 6
                        and (
                            self.currentBallPosition > 0.30000
                            and self.currentBallPosition < 0.30000 + self.ballOffset
                        )
                    ):
                        # print("third",self.endBallPosition,self.currentBallPosition,self.endBallPosition+self.ballOffset,self.currentFingerStep)
                        if self.downMove == True:
                            self.busyHand = True
                            self.prevFingerStep = self.currentFingerStep
                            self.currentBallPosition = (
                                0.26000  # 0.25000 + self.ballOffset
                            )
                            changeLocation(
                                bpy.data.objects["Sphere"],
                                "z",
                                self.currentBallPosition,
                            )
                        else:
                            self.busyHand = False
                    elif (
                        self.currentFingerStep == 6
                        and self.prevFingerStep == 7
                        and (
                            self.currentBallPosition > self.endBallPosition
                            and self.currentBallPosition < 0.25000 + self.ballOffset
                        )
                    ):
                        self.busyHand = True
                        self.prevFingerStep = self.currentFingerStep
                    else:
                        self.busyHand = False
                        self.prevFingerStep = 0
                if (
                    self.currentFingerStep == 6 or self.currentFingerStep == 7
                ) and self.busyHand == False:

                    if (
                        self.currentBallPosition > 0.30000
                        and self.currentBallPosition < 0.30000 + self.ballOffset
                    ) and self.currentFingerStep == 6:
                        self.busyHand = True
                        self.prevFingerStep = self.currentFingerStep
                    elif (
                        self.currentBallPosition > self.endBallPosition
                        and self.currentBallPosition < 0.25000 + self.ballOffset
                    ) and self.currentFingerStep == 7:
                        self.busyHand = True
                        self.prevFingerStep = self.currentFingerStep

                self.sampledData[self.sampleIndex] = list(
                    map(
                        float,
                        self.data
                        + [self.currentBallPosition]
                        + [time.time() - self.startTime]
                        + [self.currentFingerStep],
                    )
                )

                if self.busyHand == True:
                    if self.captureBallFirstTime == True:
                        self.captureBallStartSec = list(self.sampledData.values())[
                            self.sampleIndex
                        ][self.nSensors * 4 + 1]
                        self.captureBallFirstTime = False
                    elif self.captureBallFirstTime == False:
                        self.capturedBallSec += (
                            list(self.sampledData.values())[self.sampleIndex][
                                self.nSensors * 4 + 1
                            ]
                            - self.captureBallStartSec
                        )
                        self.captureBallStartSec = list(self.sampledData.values())[
                            self.sampleIndex
                        ][self.nSensors * 4 + 1]
                else:
                    self.captureBallFirstTime = True

                self.sampleIndex += 1

        if (time.time() - self.startTime) >= self.gameDuration:
            self.elapsedTime = time.time() - self.startTime
            self.gadgetConnection.finished = True
            self.gadgetConnection.stop()
            updateLeds(0)
            self.score = fistAndBall_logScore_SaveData(
                self.date,
                self.difficulty,
                self.elapsedTime,
                self.capturedBallSec,
                "Finished",
                self.sampledData,
                self.sampleIndex,
            )
            self.cancel(context)
            self.report(
                {"INFO"},
                " Finished Automatically,  {score:.2f} /100  ".format(score=self.score),
            )
            showMessageBox(
                self,
                context,
                message=" Your Score is {score:.2f} ".format(score=self.score),
            )
            context.scene.panelAccess_FistAndBall = True
            cdToFolder(self.mainDirectory)
            return {"CANCELLED"}
        if self.gadgetConnection.errorMsg == "Connection Lost":
            self.elapsedTime = time.time() - self.startTime
            self.data = []
            try:
                self.gadgetConnection.stop()
            except Exception as error:
                print(error)
            finally:
                updateLeds(0)
                self.score = fistAndBall_logScore_SaveData(
                    self.date,
                    self.difficulty,
                    self.elapsedTime,
                    self.capturedBallSec,
                    "LostConn",
                    self.sampledData,
                    self.sampleIndex,
                )
                self.cancel(context)
                self.report({"ERROR"}, " Connection To Device Has Been Lost ")
                showMessageBox(
                    self,
                    context,
                    message=" Your Score is {score:.2f} ".format(score=self.score),
                )
                context.scene.panelAccess_FistAndBall = True
                cdToFolder(self.mainDirectory)
                return {"CANCELLED"}

        return {"PASS_THROUGH"}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self.timer)

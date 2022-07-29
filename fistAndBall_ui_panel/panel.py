import bpy
from fistAndBall_modal_timer_operator.modalTimerOperator import (
    ModalTimerOperatorFistBall,
)


class FumRoboticsLabPanelFistBall(bpy.types.Panel):

    bl_label = " FUM Fist&Ball "
    bl_idname = "OBJECT_PT_FumRoboticsLab_FistBall"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Fist & Ball"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        layout.prop(context.window_manager.time, "duration", expand=True)
        layout.prop(context.window_manager.mode, "mode", expand=True)

        run = layout.operator(ModalTimerOperatorFistBall.bl_idname, text="Run")
        run.gameDuration = float(list(context.window_manager.time.duration)[0]) * 60
        run.difficulty = context.window_manager.mode.mode
        run.selectedGesture = 0
        run.selectedTag = 0

        # easy = layout.operator(ModalTimerOperatorFistBall.bl_idname, text="Easy")
        # easy.desiredSamples = 30000
        # easy.selectedGesture = 0
        # easy.selectedTag = 0
        # easy.difficulty = "Easy"

        # medium = layout.operator(ModalTimerOperatorFistBall.bl_idname, text="Medium")
        # medium.desiredSamples = 30000
        # medium.selectedGesture = 0
        # medium.selectedTag = 0
        # medium.difficulty = "Medium"

        # hard = layout.operator(ModalTimerOperatorFistBall.bl_idname, text="Hard")
        # hard.desiredSamples = 30000
        # hard.selectedGesture = 0
        # hard.selectedTag = 0
        # hard.difficulty = "Hard"
        layout.enabled = context.scene.panelAccess_FistAndBall

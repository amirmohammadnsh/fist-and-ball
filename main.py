import bpy
from bpy.props import BoolProperty
from fistAndBall_ui_panel.panel import FumRoboticsLabPanelFistBall
from fistAndBall_ui_panel.paramsControl import DurationAndModeVars
from fistAndBall_modal_timer_operator.modalTimerOperator import (
    ModalTimerOperatorFistBall,
)

bl_info = {
    "name": " Fum Robotics Lab - Fist&Ball Gadget Boards Edition ",
    "blender": (2, 93, 7),
    "author": "Amir-M Naddaf-SH",
    "description": "Try Fist and Catch the Ball",
    "version": (1, 5),
    "category": "Development",
}

classes = (ModalTimerOperatorFistBall, FumRoboticsLabPanelFistBall, DurationAndModeVars)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.time = bpy.props.PointerProperty(type=DurationAndModeVars)
    bpy.types.WindowManager.mode = bpy.props.PointerProperty(type=DurationAndModeVars)
    bpy.types.Scene.panelAccess_FistAndBall = BoolProperty(
        name="Panel Access", default=True
    )


def unregister():
    del bpy.types.WindowManager.time
    del bpy.types.WindowManager.mode
    del bpy.types.Scene.panelAccess_FistAndBall
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

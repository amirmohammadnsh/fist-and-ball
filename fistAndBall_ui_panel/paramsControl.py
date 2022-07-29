import bpy


class DurationAndModeVars(bpy.types.PropertyGroup):
    duration: bpy.props.EnumProperty(
        items=[
            ("2min", "2 Min", "duration", "", 0),
            ("4min", "4 Min", "duration", "", 1),
            ("6min", "6 Min", "duration", "", 2),
        ],
        default="2min",
    )
    mode: bpy.props.EnumProperty(
        items=[
            ("easy", "Simple", "mode", "", 0),
            ("medium", "Intermediate", "mode", "", 1),
            ("hard", "Advanced", "mode", "", 2),
        ],
        default="easy",
    )

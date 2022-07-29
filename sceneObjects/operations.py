import bpy


def sphereDraw(x, y, z, r, name):

    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, radius=r, location=[x, y, z])
    bpy.context.object.name = name
    bpy.context.object.data.name = name


def changeLocation(obj, axis, pos):
    obj.location["xyz".index(axis)] = pos

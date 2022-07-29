import bpy
from sceneObjects.operations import sphereDraw

def createAndPlaceBall(beginBallPosition):
    avlObjects = list(bpy.data.objects)
    for obj in avlObjects:

        if obj.name == "Sphere":
            bpy.data.objects["Sphere"].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects["Sphere"]
            bpy.ops.object.delete()

    sphereDraw(-0.02, 0.47, beginBallPosition, 0.16, "Sphere")
    bpy.context.view_layer.objects.active = bpy.data.objects["Sphere"]
    materials = list(bpy.data.materials)
    avlMat = False
    for mat in materials:
        if mat.name == "ballColor":
            mesh = bpy.context.object.data
            mesh.materials.append(mat)
            avlMat = True

        if avlMat == False:
            ballMat = bpy.data.materials.new("ballColor")
            ballMat.diffuse_color = (40.460, 1.078, 0.393, 0.8)
            mesh = bpy.context.object.data
            mesh.materials.clear()
            mesh.materials.append(ballMat)
        bpy.context.active_object.select_set(False)



import bpy


def createAndPlace9Leds():
    # avlObjects = list(bpy.data.objects)
    # for obj in avlObjects:
    #     if "LED" in obj.name:
    #         ledObjects.append(obj)

    materials = list(bpy.data.materials)
    avlMat = False
    for mat in materials:
        if mat.name == "LEDRED":
            avlMat = True
            for i in range(1, 10):
                bpy.data.objects["LED" + str(i)].data.materials.clear()
                bpy.data.objects["LED" + str(i)].data.materials.append(mat)
    if avlMat == False:

        ledRedMat = bpy.data.materials.new("LEDRED")
        ledRedMat.diffuse_color = (1, 0, 0, 1)
        for i in range(1, 10):
            bpy.data.objects["LED" + str(i)].data.materials.append(ledRedMat)
    avlMat = False
    materials = list(bpy.data.materials)
    for mat in materials:
        if mat.name == "LEDGREEN":
            avlMat = True
            break
    if avlMat == False:
        ledGreenMat = bpy.data.materials.new("LEDGREEN")
        ledGreenMat.diffuse_color = (0, 1, 0, 1)


def updateLeds(fingerStep):
    greenMat = bpy.data.materials.get("LEDGREEN")
    redMat = bpy.data.materials.get("LEDRED")
    totalLeds = 9
    onLeds = fingerStep
    # offLeds = totalLeds - onLeds

    for i in range(1, onLeds + 1):

        bpy.data.objects["LED" + str(i)].data.materials.clear()
        bpy.data.objects["LED" + str(i)].data.materials.append(greenMat)
    if fingerStep != 9:
        for i in range(onLeds + 1, totalLeds + 1):

            bpy.data.objects["LED" + str(i)].data.materials.clear()
            bpy.data.objects["LED" + str(i)].data.materials.append(redMat)

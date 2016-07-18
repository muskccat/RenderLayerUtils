# coding : euc-kr
# Camera clip plane creator
#
# 2016.07.18
# ver 1.0
# by Musky

import maya.cmds as cmds
import maya.mel as mel

# create clip plane (Poly Plane)

def make_plane(name):
    plane = cmds.polyPlane(n=name,w=1,h=1,sx=1,sy=1)
    pShape = cmds.listRelatives(plane,s=True)
    pShape = pShape[0]
    plane = plane[0]
    cmds.setAttr(pShape +".castsShadows", 0)
    cmds.setAttr(pShape +".receiveShadows", 0)
    cmds.setAttr(pShape +".motionBlur", 0)
    cmds.setAttr(pShape +".primaryVisibility", 0)
    cmds.setAttr(pShape +".smoothShading" ,0)
    cmds.setAttr(pShape +".visibleInReflections", 0)
    cmds.setAttr(pShape +".visibleInRefractions", 0)
    cmds.setAttr(pShape +".doubleSided", 0)

    # cmds.setAttr(plane+".hiddenInOutliner", 1)
    cmds.setAttr(plane+".overrideEnabled",1)
    cmds.setAttr(plane+".overrideShading",0)
    cmds.setAttr(plane+".overrideColor",17)

    planes = (plane, pShape)

    return planes



def clip_plane_creator(*args):
    gui = 'clipPlaneCreator'
    
    if cmds.window(gui, q=1, ex=1):
        cmds.deleteUI(gui)

    cmds.window(gui,t="Clip Plane Creator v1.0")
    cmds.columnLayout(adjustableColumn = True)
    
    cms = cmds.ls(typ="camera")
    cm_list = []
    for x in cms:
        ortho = cmds.getAttr(x+".orthographic")
        p = cmds.listRelatives(x,p=True)
        if not(ortho) : cm_list.append(p[0])
    
    cmds.text("Camera List", h = 30)
    cmds.textScrollList('cam_sel',append = cm_list,ams=False)
    cmds.separator()
        
    cmds.window(gui, e=1, width=360, height = 120)
    cmds.showWindow(gui)
    
clip_plane_creator()
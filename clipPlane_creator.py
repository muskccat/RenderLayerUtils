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
    # It doesn't show in Outliner. (On purpose, it was hidden)
    
    cmds.setAttr(plane+".overrideEnabled",1)
    cmds.setAttr(plane+".overrideShading",0)
    cmds.setAttr(plane+".overrideColor",17)
    cmds.setAttr(plane+".rx", 90)
    cmds.setAttr(plane + ".tx", lock=True, k=False, channelBox = False)
    cmds.setAttr(plane + ".ty", lock=True, k=False, channelBox = False)
    cmds.setAttr(plane + ".tz", lock=True, k=False, channelBox = False)
    cmds.setAttr(plane + ".rx", lock=True, k=False, channelBox = False)
    cmds.setAttr(plane + ".ry", lock=True, k=False, channelBox = False)
    cmds.setAttr(plane + ".rz", lock=True, k=False, channelBox = False)
    cmds.setAttr(plane + ".sx", lock=True, k=False, channelBox = False)
    cmds.setAttr(plane + ".sy", lock=True, k=False, channelBox = False)
    cmds.setAttr(plane + ".sz", lock=True, k=False, channelBox = False)
    
    
    planes = (plane, pShape)

    return planes
    
def g_plane(*args):
    
    # create a null & define name
    for i, x in enumerate(args):
        cmds.select(cl=True)
        x = cmds.Group()
        n1 = cmds.ls(sl=True)
        cmds.rename(n1,args[i])

        
    return args
    

    
            
    
def c_plane(*ars):
    name = cmds.textScrollList('cam_sel', q=True, si=True)
    print name
    
    def make_tex(*args):
        tex = []
        for x in args:
            x = cmds.textCurves( ch=False, f="Arial|w400|h-11", t=x)
            tex.append(x)
        return tex
    
    if name==None : print "Please select a camera."
    else :
        if not(cmds.objExists(name[0] + "_clipPlane")):
            cp = make_plane(name[0]+"_clipPlane")
            g = g_plane(name[0] + "_nearClipping", name[0]+"_farClipping")
            t = make_tex("NEAR CLIP PLANE", "FAR CLIP PLANE")
            
            for i,x in enumerate(g) :
                cmds.parent(x,name[0])
                cmds.setAttr(x+".translate",0,0,0)
                cmds.setAttr(x+".rotate",0,0,0)
                cmds.setAttr(x+".scale",1,1,1)

                cmds.parent(t[i], x)
                tex = t[i]
                cmds.setAttr(tex[0]+".translate",0,0,0)
                cmds.setAttr(tex[0]+".rotate",0,0,0)
                cmds.setAttr(tex[0]+".scale",.1,.1,.1)
                cmds.setAttr(tex[0] + ".tx", lock=True, k=False, channelBox = False)
                cmds.setAttr(tex[0] + ".ty", lock=True, k=False, channelBox = False)
                cmds.setAttr(tex[0] + ".tz", lock=True, k=False, channelBox = False)
                cmds.setAttr(tex[0] + ".rx", lock=True, k=False, channelBox = False)
                cmds.setAttr(tex[0] + ".ry", lock=True, k=False, channelBox = False)
                cmds.setAttr(tex[0] + ".rz", lock=True, k=False, channelBox = False)
                cmds.setAttr(tex[0] + ".sx", k=False, channelBox = False)
                cmds.setAttr(tex[0] + ".sy", k=False, channelBox = False)
                cmds.setAttr(tex[0] + ".sz", k=False, channelBox = False)
                
                cmds.select(cp[0],r=True)
                cmds.select(x,add=True)
                cmds.parent(add=True)
                
                
            


def clip_plane_creator(*args):
    gui = 'clipPlaneCreator'
    
    if cmds.window(gui, q=1, ex=1):
        cmds.deleteUI(gui)

    cmds.window(gui,t="Clip Plane Creator v1.0")
    cmds.columnLayout(adjustableColumn = True)
    
    # Get perspective camera (Not orthographic)
    cms = cmds.ls(typ="camera")
    cm_list = []
    cmt = lambda x:cmds.listRelatives(x, p=True)    # get camera's transform node
    cm_list = filter(lambda x:not(cmds.getAttr(x+".orthographic")), cms)    # if orthographic is true, doesn't append "cm_list var"
    cm_list = cmt(cm_list)
    
    
    cmds.text("Camera List", h = 30)
    cmds.textScrollList('cam_sel',append = cm_list,ams=False)
    cmds.separator()
    cmds.button('bCreatePlane', label = "Create Clip Plane", width = 200, c = c_plane)
    cmds.window(gui, e=1, width=360, height = 120)
    cmds.showWindow(gui)
    
clip_plane_creator()
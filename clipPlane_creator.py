# coding : euc-kr
# Camera clip plane creator
#
# 2016.07.18
# ver 1.0
# by Musky

import maya.cmds as cmds
import maya.mel as mel

# create clip plane (Poly Plane)


def obj_del(obj):
    if cmds.objExists(obj) :
        cmds.delete(obj)
        
def lock_attr(obj, trs, l, k, c):
    
    cmds.setAttr(obj +"."+ trs+"x", lock=l, k=k, channelBox = c)
    cmds.setAttr(obj +"."+ trs+"y", lock=l, k=k, channelBox = c)
    cmds.setAttr(obj +"."+ trs+"z", lock=l, k=k, channelBox = c)
        
        

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
        np = name[0]+"_nearClipPlane"
        fp = name[0]+"_farCipPlane"
        obj_del(np)
        obj_del(fp)
            
        g = (make_plane(np), make_plane(fp))
        dist = (cmds.floatField('vNear',q=True,v=True) ,cmds.floatField('vFar',q=True,v=True))
        #cmds.setAttr(cp[1]+".overrideEnabled", 1)
        #cmds.setAttr(cp[1]+".overrideDisplayType", 1)
        
        for i,x in enumerate(g) :
            x = x[0]
            cmds.parent(x,name[0])
            cmds.setAttr(x+".translate",0,0,0)
            cmds.setAttr(x+".rotate",-90,0,0)
            cmds.setAttr(x+".scale",1,1,1)
      
            lock_attr(x,"t",True,False,False)
            lock_attr(x,"r",True,False,False)
            #lock_attr(x,"s",True,False,False)
            cmds.setAttr(x+".tz", lock=False,k= True, channelBox = True)
            cmds.setAttr(x+".tz",-dist[i])
        cmds.select(name[0],r=True)
    

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
    
   
    cmds.button('cam_list', l = "Camera List", h = 30,bgc=(0.4,0.4,1), c=clip_plane_creator )
    cmds.textScrollList('cam_sel',append = cm_list,ams=False , h = 180)
    cmds.separator()
    cmds.rowColumnLayout(numberOfColumns = 4)
    cmds.text("Near Dist:",w = 60)
    cmds.floatField('vNear', v = 10,width = 60)
    cmds.text("Far Dist:", w= 60)
    cmds.floatField('vFar',  v = 100, w= 60)
    cmds.setParent("..")
    
    cmds.button('bCreatePlane', label = "Create Clip Plane", width = 200, c = c_plane)
    cmds.window(gui, e=1, width=240, height = 120)
    cmds.showWindow(gui)
    
clip_plane_creator()

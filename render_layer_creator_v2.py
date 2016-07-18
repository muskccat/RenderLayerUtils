# coding : euc-kr
# MARO render-layer creation script
#
# 2016.07.18
# ver 2.0
# by Musky

import maya.cmds as cmds
import maya.mel as mel


# SHADER Creator
def make_shd(name, rgb, type):

    #Set Frame/Animation Ext to name_#.ext
    cmds.setAttr("defaultRenderGlobals.outFormatControl",0)
    cmds.setAttr("defaultRenderGlobals.animation",1)
    
    #set shader & shadingGroup name 
    s_name = "M_" + name+ "_mat"
    sg_name= "M_" + name + "_SG"
    s_type = ('surfaceShader', 
              'useBackground',
              'surfaceShader', 
              'surfaceShader'
              )
    

    # RGB Mask Shader
    def set_color(n,rgb):    #rgb must be a tuple.
        cmds.setAttr(n+".outColor",rgb[0],rgb[1],rgb[2],type="double3")

    # Shadow Shader (useBackground)
    def set_shadow(n):
        cmds.setAttr(n+".specularColor",0,0,0, type='double3')
        cmds.setAttr(n+".reflectivity", 0)
        cmds.setAttr(n+".reflectionLimit",0)
        cmds.setAttr(n+".shadowMask",1)
        
    # Ambient Occlusion Shader (mentalRay)
    def set_ao(n):
        oc = mel.eval("mrCreateCustomNode -asTexture \"\" mib_amb_occlusion")
        cmds.connectAttr(oc+".outValue", n+".outColor", f=True)
        cmds.setAttr(oc+".samples", 264)
        cmds.setAttr(oc+".max_distance", 1.0)

    
    # zDepth Shader 
    def set_depth(n):        
    
        cmds.addAttr(n,ln="close", at="double", min=0)
        cmds.addAttr(n,ln="far", at="double", min=0)
        cmds.setAttr(n+".far", 1000,e=True,keyable=True)
        cmds.setAttr(n+".close",10, e=True,keyable=True)
        
        zr = cmds.shadingNode("ramp",n="zDepth_ramp", asTexture=True)
        zps = cmds.shadingNode("samplerInfo",n="zDepth_samplerInfo",asUtility=True)
        zdb = cmds.shadingNode("distanceBetween",n="zDepth_distanceBetween",asUtility=True)
        zsr = cmds.shadingNode("setRange",n="zDepth_setRange",asUtility=True)
        
        cmds.removeMultiInstance(zr+'.colorEntryList[1]', b=True)
        cmds.setAttr(zr+'.colorEntryList[2].color',0,0,0, type='double3')
        cmds.setAttr(zr+'.colorEntryList[2].position',1)
        cmds.setAttr(zr+'.colorEntryList[0].color',1,1,1, type='double3')
        cmds.setAttr(zr+'.interpolation', 3,)
        
        cmds.connectAttr(zsr+".outValueX", zr+".vCoord")
        cmds.connectAttr(zdb+".distance", zsr+".valueX")
        cmds.connectAttr(zps+".pointCamera",zdb+".point1")
        cmds.connectAttr(n+".far", zsr+".oldMaxX")
        cmds.connectAttr(n+".close", zsr+".oldMinX")
        cmds.connectAttr(zr+".outColor",n+".outColor")
        
        
  # Maker Shader
    if not(cmds.objExists(s_name)): #Check that M_***_mat exists       
        cmds.shadingNode(s_type[type-1],n=s_name,asShader=True ) #Black_mat Shader Create
        cmds.sets(n=sg_name, renderable=True, noSurfaceShader=True, empty=True) #Set Shading Group
        cmds.connectAttr(s_name+".outColor", sg_name+".surfaceShader", f=True) #Connect shader to shading group
        
        if type == 1: set_color(s_name,rgb)
        if type == 2: set_shadow(s_name)         
        if type == 3: set_ao(s_name)
        if type == 4: set_depth(s_name)

# Shaders create loop function
def shd_creation():
    shd_list = {'BLACK':((0,0,0),1),
                'BLUE':((0,0,1),1),
                'GREEN':((0,1,0),1),
                'RED':((1,0,0),1),
                'Shadow':((0,0,0),2),
                'AO':((0,0,0),3),
                'zDepth':((0,0,0),4)}   # Shader Key List
    
    name = shd_list.keys()
    for n in name:
        x = shd_list[n]
        make_shd(n,x[0],x[1])

# Create Render Layer
def make_layer(name,sf,ef, r_type):
    rl_name = name

    l = cmds.createRenderLayer(n=rl_name, number=2,noRecurse=True)
    cmds.editRenderLayerGlobals(crl=l)
    cmds.editRenderLayerAdjustment("defaultRenderGlobals.imageFilePrefix")
    cmds.editRenderLayerAdjustment("defaultRenderGlobals.imageFormat")
   
    drg = "defaultRenderGlobals"
    cmds.setAttr(drg+".imageFilePrefix",rl_name,typ="string")
    cmds.setAttr(drg+".imageFormat",32)
    cmds.setAttr(drg + ".startFrame", sf)
    cmds.setAttr(drg + ".endFrame", ef)
    
    if (r_type == "AO"):
        cmds.editRenderLayerAdjustment(drg+".currentRenderer")
        cmds.setAttr(drg+".ren","mentalRay",typ="string")

     
    return l


def get_name(type):
    
    name =  "EP_" + cmds.textFieldGrp('ep_field',q=True,text=True) +  "_SC" + cmds.textFieldGrp('sc_field',q=True,text=True) +  "_C"  + cmds.textFieldGrp('cn_field',q=True,text=True) +"_"   + cmds.textFieldGrp('ex_field',q=True,text=True) 
    cb = cmds.checkBox('c_box', q=True,  v=True)
    cus = cmds.textFieldGrp('cus', q=True, text=True)
 
    if cb : name = cus
    else  : name = name + "_" + type   

    return name


def bRgb_mask(*args):
    type = "RGB_Mask"
    name = get_name(type)    
    sf = int(cmds.textFieldGrp('start_frame', q=True, tx=True))
    ef = int(cmds.textFieldGrp('end_frame', q=True, tx=True))
    make_layer(name, sf, ef, type)

def bNormal(*args):
    type = "Normal"
    name = get_name(type)    
    sf = int(cmds.textFieldGrp('start_frame', q=True, tx=True))
    ef = int(cmds.textFieldGrp('end_frame', q=True, tx=True))
    make_layer(name, sf, ef, type)    
    
def bAO(*args):
    type = "AO"
    name = get_name(type)    
    sf = int(cmds.textFieldGrp('start_frame', q=True, tx=True))
    ef = int(cmds.textFieldGrp('end_frame', q=True, tx=True))
    make_layer(name, sf, ef, type)    


def bZDepth(*args):
    type = "zDepth"
    name = get_name(type)    
    sf = int(cmds.textFieldGrp('start_frame', q=True, tx=True))
    ef = int(cmds.textFieldGrp('end_frame', q=True, tx=True))
    make_layer(name, sf, ef, type)    
    
def bEmpty(*args):
    type = ""
    name = get_name(type)    
    sf = int(cmds.textFieldGrp('start_frame', q=True, tx=True))
    ef = int(cmds.textFieldGrp('end_frame', q=True, tx=True))
    make_layer(name, sf, ef, type)    



def mrl_base_gui(*ars):
    gui = 'mrl_gui'
    
    if cmds.window(gui, q=1, ex=1):
        cmds.deleteUI(gui)

    cmds.window(gui,t="Render Layer Creator v2.0")
    shd_creation() # if default shader don't exist then create new shader.
    cmds.columnLayout(adjustableColumn = True)
    
    cmds.textFieldGrp('ep_field', label='Episode',columnAlign=(1,'both'),columnWidth=(1,80))
    cmds.textFieldGrp('sc_field',label='Scene Number', columnAlign=(1,'both'),columnWidth=(1,80))
    cmds.textFieldGrp('cn_field', label='Cut Number', columnAlign=(1,'both'),columnWidth=(1,80))
    cmds.textFieldGrp('ex_field',label='Explanation',  columnAlign=(1,'both'),columnWidth=(1,80))
    cmds.checkBox('c_box', label = 'Use a custom name')
    cmds.textFieldGrp('cus',label='Custom',  columnAlign=(1,'both'),columnWidth=(1,80))
    cmds.separator()
        
    sf = int(cmds.playbackOptions(q=True,ast=True))
    ef = int(cmds.playbackOptions(q=True,aet=True))
    cmds.textFieldGrp('start_frame',label='Start Frame',tx = sf,columnAlign=(1,'both'),columnWidth=(1,80))  
    cmds.textFieldGrp('end frame', label='End Frame', tx = ef, columnAlign=(1,'both'),columnWidth=(1,80))
    
    cmds.rowColumnLayout(numberOfRows=2)
    cmds.button('rgb_mask', label= "RGB Mask", width=120, c=bRgb_mask)
    cmds.button('normal', label= "Normal", width=120, c=bNormal)
    cmds.button('AO', label= "AO", width=120, c=bAO)
    cmds.button('zDepth', label= "zDepth", width=120, c=bZDepth)
    cmds.button('empty', label= "empty", width=120, c=bEmpty)
    
    cmds.button( label ="Refresh",width=120, command=mrl_base_gui)
    cmds.window(gui, e=1, width=360, height = 120)
    cmds.showWindow(gui)


mrl_base_gui()
cmds.select(cl=True)
    
    

        

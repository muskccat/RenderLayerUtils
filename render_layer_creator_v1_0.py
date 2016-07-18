# coding : euc-kr
# MARO render-layer creation script
# 
# 2016.07.13
# ver 1.0
# by musky

import maya.cmds as cmds
import maya.mel as mel
 
 
def make_shd(name, rgb, type):
    #set shader & shadingGroup name 
    s_name = "M_" + name+ "_mat"
    sg_name= "M_" + name + "_SG"
    s_type = ('surfaceShader', 'useBackground','surfaceShader')
    
    def set_color(n,rgb):    #rgb must be a tuple.
        cmds.setAttr(n+".outColor",rgb[0],rgb[1],rgb[2],type="double3")
        
    def set_shadow(n):
        cmds.setAttr(n+".specularColor",0,0,0, type='double3')
        cmds.setAttr(n+".reflectivity", 0)
        cmds.setAttr(n+".reflectionLimit",0)
        cmds.setAttr(n+".shadowMask",1)
        
    def set_ao(n):
        oc = mel.eval("mrCreateCustomNode -asTexture \"\" mib_amb_occlusion")
        cmds.connectAttr(oc+".outValue", n+".outColor", f=True)
        cmds.setAttr(oc+".samples", 264)
        cmds.setAttr(oc+".max_distance", 1.0)
        
        
    if not(cmds.objExists(s_name)): #Check that M_***_mat exists       
        cmds.shadingNode(s_type[type-1],n=s_name,asShader=True ) #Black_mat Shader Create
        cmds.sets(n=sg_name, renderable=True, noSurfaceShader=True, empty=True) #Set Shading Group
        cmds.connectAttr(s_name+".outColor", sg_name+".surfaceShader", f=True) #Connect shader to shading group
        
        if type == 1: set_color(s_name,rgb)
        if type == 2: set_shadow(s_name)         
        if type == 3: set_ao(s_name)


def shd_creation():
    shd_list = {'BLACK':((0,0,0),1),'BLUE':((0,0,1),1), 'GREEN':((0,1,0),1), 'RED':((1,0,0),1),'Shadow':((0,0,0),2),'AO':((0,0,0),3)}
    name = shd_list.keys()
    for n in name:
        x = shd_list[n]
        make_shd(n,x[0],x[1])


def make_layer(n,cus,sw):
    if sw:
        l = cmds.createRenderLayer(n=cus, number=2,noRecurse=True)
    else:
        l = cmds.createRenderLayer(n=n, number=2,noRecurse=True)
    return l

def mrl_base_gui():

    if cmds.window('mrl_gui', q=1, ex=1):
        cmds.deleteUI('mrl_gui')
        
    cmds.window('mrl_gui',t="Render Layer Creator")
    shd_creation() # if default shader don't exist then create new shader.
    cmds.columnLayout(adjustableColumn = True)
    
    #Episode + Scene Numbering & Additional Explanation
    ep = cmds.textFieldGrp( label='Episode',columnAlign=(1,'both'),columnWidth=(1,80))
    sc = cmds.textFieldGrp( label='Scene Number', columnAlign=(1,'both'),columnWidth=(1,80))
    exp = cmds.textFieldGrp( label='Explanation',  columnAlign=(1,'both'),columnWidth=(1,80))
    cb = cmds.checkBox(label = 'Use a custom name')
    cus = cmds.textFieldGrp( label='Custom',  columnAlign=(1,'both'),columnWidth=(1,80))

    
    cmds.rowColumnLayout(numberOfRows=2)
    cmds.button( label = "RGB Mask",width = 120,
    command=lambda x:make_layer("EP"+cmds.textFieldGrp(ep,text=True,q=True)
                                +"_C"+cmds.textFieldGrp(sc,text=True,q=True)                        
                                +"_"+cmds.textFieldGrp(exp,text=True,q=True)+"_RGB_mask",
                                cmds.textFieldGrp(cus,text=True,q=True),cmds.checkBox(cb,q=True,v=True)))
                                                                            
    cmds.button( label = "Normal",width = 120, 
    command=lambda x:make_layer("EP"+cmds.textFieldGrp(ep,text=True,q=True)
                                +"_C"+cmds.textFieldGrp(sc,text=True,q=True)                        
                                +"_"+cmds.textFieldGrp(exp,text=True,q=True)+"_Normal",
                                cmds.textFieldGrp(cus,text=True,q=True),cmds.checkBox(cb,q=True,v=True)))
                                                                            
    cmds.button( label = "AO",width = 120,
    command=lambda x:make_layer("EP"+cmds.textFieldGrp(ep,text=True,q=True)
                                +"_C"+cmds.textFieldGrp(sc,text=True,q=True)                        
                                +"_"+cmds.textFieldGrp(exp,text=True,q=True)+"_AO",
                                cmds.textFieldGrp(cus,text=True,q=True),cmds.checkBox(cb,q=True,v=True)))
                                
    cmds.button( label = "zDepth",width = 120,
    command=lambda x:make_layer("EP"+cmds.textFieldGrp(ep,text=True,q=True)
                                +"_C"+cmds.textFieldGrp(sc,text=True,q=True)                        
                                +"_"+cmds.textFieldGrp(exp,text=True,q=True)+"_zDepth",
                                cmds.textFieldGrp(cus,text=True,q=True),cmds.checkBox(cb,q=True,v=True)))
                                
    cmds.button( label = "empty",width = 120,
    command=lambda x:make_layer("EP"+cmds.textFieldGrp(ep,text=True,q=True)
                                +"_C"+cmds.textFieldGrp(sc,text=True,q=True)                        
                                +"_"+cmds.textFieldGrp(exp,text=True,q=True)+"_",
                                cmds.textFieldGrp(cus,text=True,q=True),cmds.checkBox(cb,q=True,v=True)))
                                
        
    cmds.window('mrl_gui', e=1, width=360, height = 120)
    cmds.showWindow('mrl_gui')


mrl_base_gui()
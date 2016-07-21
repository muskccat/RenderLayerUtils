# coding : euc-kr
# MARO Render layer Rename
# 
# 2016.07.21
# ver 1.0
# by musky

import maya.cmds as cmds
import maya.mel as ml
import types

def ch_name(*args):
    name = cmds.textScrollList('rl_list',q=True,si=True)
    n_name = cmds.textFieldGrp('ch_name',q=True, text=True)
    i_name = cmds.textFieldGrp('ch_fname',q=True, text=True)
    if type(name) != types.NoneType:
        cmds.rename(name[0],n_name)
        cmds.editRenderLayerGlobals(crl=n_name)
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix", n_name+"_"+i_name, typ="string")
        rl = cmds.ls(typ="renderLayer")
        rls = filter (lambda x:x !="defaultRenderLayer", rl)
        cmds.textScrollList('rl_list', e=True,ra=True,append =rls ,ams=False)
    
def img_name(*args):
    name = cmds.textScrollList('rl_list',q=True,si=True)
    if type(name) != types.NoneType:
        cmds.editRenderLayerGlobals(crl=name[0])
        i_n = cmds.getAttr("defaultRenderGlobals.imageFilePrefix")
        cmds.textScrollList('img_list', e=True,ra=True,ams=False,append=i_n)

# Main GUI
def ren_gui(*ars):
    gui = 'ren_gui'
    
    if cmds.window(gui, q=1, ex=1):
        cmds.deleteUI(gui)

    cmds.window(gui,t="Render Layer name changer v1.0")
    cmds.columnLayout(adjustableColumn = True)
    
    cmds.text("Select Render Layer", bgc=(.3,.1,.1), h = 25)
    
    rl = cmds.ls(typ="renderLayer")
    rls = filter (lambda x:x !="defaultRenderLayer", rl)
    
    cmds.rowColumnLayout(numberOfColumns = 2)
    cmds.textScrollList('rl_list', append=rls, ams=False, sc=img_name)
    cmds.textScrollList('img_list', append="", ams=False)
    
    cmds.setParent("..")    
    cmds.button('bCh', label="RENDER LAYER RENAME", bgc=(0.5,0.7,0.9), c=ch_name)    
    cmds.textFieldGrp('ch_name', label="Input new name:",cal=(1,"left") ,cw=(1,95))
    cmds.textFieldGrp('ch_fname', label="Img name suffix:",cal=(1,"left") ,cw=(1,95))
    
    

    
    
        
    cmds.window(gui, e=1, width=360, height = 120)
    cmds.showWindow(gui)
    
ren_gui()
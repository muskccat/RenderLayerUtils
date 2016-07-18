# coding : euc-kr
# MARO Object to render layer
# 
# 2016.07.13
# ver 1.0
# by musky

import maya.cmds as cmds
import maya.mel as ml


def put_obj(obj,rl):
    for x in obj:
        cmds.editRenderLayerMembers(rl[0],x,noRecurse=True)

def rgb_base_gui(*args):

    if cmds.window('rgb_gui', q=1, ex=1):
        cmds.deleteUI('rgb_gui')
        
    cmds.window('rgb_gui', t="Object to Render layer")
    cmds.columnLayout(adjustableColumn = True)
    cmds.rowColumnLayout(numberOfColumns=2)
    sels = cmds.ls(sl=1)
    rls = cmds.ls(typ="renderLayer")
    rl = []
    for x in rls:
        if x != "defaultRenderLayer":
            rl.append(x)

    
    objs = cmds.textScrollList(append=sels,ams=True,height = 450)
    rls = cmds.textScrollList(append=rl,ams=False)
        
    cmds.rowColumnLayout(numberOfRows=2)
    cmds.button( label = "REFRESH",width = 150,command = rgb_base_gui)
    cmds.button( label = "Assign",width = 150, command = lambda x:put_obj(cmds.textScrollList(objs,q=True,si=True), cmds.textScrollList(rls,q=True,si=True)))
    cmds.window('rgb_gui', e=1, width=450, height = 250)
    cmds.showWindow('rgb_gui')
    
    
rgb_base_gui()
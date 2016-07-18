# coding : euc-kr
# MARO Assign Mask Shader script
# 
# 2016.07.13
# ver 1.0
# by musky

import maya.cmds as cmds
import maya.mel as mel


def assign_shd(obj,c):
    color = ["M_RED_mat",  "M_GREEN_mat", "M_BLUE_mat"]
    for x in obj:
        #cmds.sets(color[c],e=True, forceElement=True)
        cmds.select(x,r=1)
        cmds.hyperShade(assign =color[c])

def assign_shd_gui(*args):

    if cmds.window('assign_gui', q=1, ex=1):
        cmds.deleteUI('assign_gui')
        
    cmds.window('assign_gui',t = "Assign Mask Shader",rtf=True)
    cmds.columnLayout(adjustableColumn = True)

    cmds.rowColumnLayout(numberOfRows=3)
    cmds.button( label = "RED",width = 350,height=120,command =  lambda x:assign_shd( cmds.ls(sl=1) ,0) )
    cmds.button( label = "GREEN",width = 350,height=120,command =  lambda x:assign_shd( cmds.ls(sl=1),1) )
    cmds.button( label = "BLUE",width = 350,height=120,command =  lambda x:assign_shd( cmds.ls(sl=1) ,2) )
    cmds.window('assign_gui',e=1, width=350,height=360)
    cmds.showWindow('assign_gui')
    
    
assign_shd_gui()
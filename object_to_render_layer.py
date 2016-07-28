# coding : euc-kr
# MARO Object to render layer
# 
# 2016.07.21
# ver 1.5
# by musky

import maya.cmds as cmds
import maya.mel as ml
import types


def put_obj(*args):    
    rl = cmds.textScrollList('rls', q=True,si=True)
    if type(rl) !=types.NoneType:
        sels = cmds.textScrollList('sels',q=True,ai=True)
        if type(sels) !=types.NoneType:
            for y in rl:
                for x in sels:
                    cmds.editRenderLayerMembers(y,x,noRecurse=True)
            rl_obj_list()
                
def rl_obj_list(*args):    
    rl = cmds.textScrollList('rls', q=True,si=True)
    if type(rl) !=types.NoneType:
        obj = get_obj(rl)
        if type(obj) != types.NoneType : cmds.textScrollList('objs',e=True, ra=True,append = obj )
        else : cmds.textScrollList('objs',e=True, ra=True,append = "")
    
def sel_objs(*args):
    sels = cmds.ls(sl=True)
    cmds.textScrollList('sels',e=True, ra=True,append = sels )
    
   
def get_obj(rl):
    if type(rl)!=types.NoneType:
        rList =[]
        for x in rl:
            rInfo = x+".renderInfo"
            li = cmds.listConnections(rInfo, d=True)
            if type(li) != types.NoneType: rList +=li;
    
        return rList
    else : return rl

def remove_objs(*ars):
        
    rl = cmds.textScrollList('rls', q=True,si=True)
    if type(rl) !=types.NoneType:
        obj = cmds.textScrollList('objs',q=True,si=True)
        if type(obj) != types.NoneType:
            for r in rl:
                for x in obj:
                    cmds.editRenderLayerMembers(r,x,remove=True,nr=True)
            rl_obj_list()
    

def rgb_base_gui(*args):

    if cmds.window('rgb_gui', q=1, ex=1):
        cmds.deleteUI('rgb_gui')
        
    cmds.window('rgb_gui', t="Object to Render layer")
    cmds.columnLayout(adjustableColumn = True)
    cmds.rowColumnLayout(numberOfColumns=3)
    cmds.text("Render Layer", h= 20, bgc= (0.3,0.6,0.8))
    cmds.text("Added Object", h= 20, bgc= (0.7,0.6,0.6))
    cmds.button("Selected Object", h = 20, bgc =(0.7,0.3,0.3),c = sel_objs)
    
    sels = cmds.ls(sl=1)
    rls = cmds.ls(typ="renderLayer")
    rl = filter(lambda x:x !="defaultRenderLayer", rls)            

    rls = cmds.textScrollList('rls', append=rl,ams=True,  sc = rl_obj_list)
    objs = cmds.textScrollList('objs', append=sels,ams=True,height = 450,bgc = (0.3,0.3,0.5))
    sels = cmds.textScrollList('sels', append=sels,ams=True,height = 450)
    
    cmds.button("REFRESH", c= rgb_base_gui)
    cmds.button("REMOVE", c=remove_objs,bgc = (0.7,0.6,0.6))
    cmds.button("ASSIGN", c= put_obj, bgc = (0.7,0.3,0.3))
    

        
    cmds.rowColumnLayout(numberOfRows=2)

    cmds.window('rgb_gui', e=1, width=450, height = 250)
    cmds.showWindow('rgb_gui')
    
    
rgb_base_gui()
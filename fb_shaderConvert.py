import maya.cmds as cmds

# Get shading group
def getSg(name):
    cOut = name+".outColor"
    sg = cmds.connectionInfo(cOut,dfs=True)
    return sg[0]

def colorCheck(name,shdNum):
#shdNum 1 : surfaceShader
#shdNum 2 : rampShader
    check = 1

    if (shdNum == 1):
        check = 1
        cc = name +".outColor"
        ci = cmds.connectionInfo(cc,sfd=True)    
        if (ci=="") :
            ci = cmds.getAttr(cc)
            ci = ci[0]
            check = 0
            
    if (shdNum == 2):
        check = 1
        cc = name +".color[0].color_Color"
        ci = cmds.connectionInfo(cc,sfd=True)    
        if (ci=="") :
            ci = cmds.getAttr(cc)
            ci = ci[0]
            check = 0

    return (check, ci)   

# Create Furryball Material
def toonCreate(name):
    sg = getSg(name)
    cmds.delete(name)
    shd = cmds.shadingNode('furryballMaterial', asShader = True, n = name)
    cmds.connectAttr( x+".outColor", sg, f=True)
    return shd
    
def ambConnect(name):
    
    amb = name+".ambientColor"
    con = cmds.connectionInfo(amb, sfd=True)
    
    if (con =="") :
        multNode = cmds.shadingNode("multiplyDivide", asUtility=True, n=name+"_ambMultDiv")
        cmds.connectAttr(multNode+".output", name+".ambientColor")      
            
        if (not cmds.objExists("ambRemapColor1")):
            remapNode = cmds.shadingNode("remapColor", asUtility=True, n="ambRemapColor1")
        else : remapNode = "ambRemapColor1"
        
        cmds.connectAttr(remapNode+".outColor", multNode+".input1", f=True)

    return multNode

      

        
# Get shader array
ss = cmds.ls(typ="surfaceShader")
rs = cmds.ls(typ="rampShader")



for x in ss:
    cc = colorCheck(x,1)
    shd = toonCreate(x)
    
    if (cc[0] == 1) :
        cmds.connectAttr(cc[1], shd+".color")
        #mult = ambConnect(x)
        #cmds.connectAttr(cc[1], mult+".input2", f=True)
        
    else:
        cmds.setAttr(shd+".color", cc[1][0], cc[1][1], cc[1][2])
        #mult = ambConnect(x)
        #cmds.setAttr(mult+".input2", cc[1][0], cc[1][1], cc[1][2])


for x in rs:
    cc = colorCheck(x,2)
    shd = toonCreate(x)
    
    if (cc[0] == 1) :
        cmds.connectAttr(cc[1], shd+".color")
        #mult = ambConnect(x)
        #cmds.connectAttr(cc[1], mult+".input2", f=True)
        
    else:
        cmds.setAttr(shd+".color", cc[1][0], cc[1][1], cc[1][2])
        #mult = ambConnect(x)
        #cmds.setAttr(mult+".input2", cc[1][0], cc[1][1], cc[1][2])


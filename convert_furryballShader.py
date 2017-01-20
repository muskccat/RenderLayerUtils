import maya.cmds as cmds

# Check color attribute is connected.
def colorCheck(name):
    check = 1
    cc = name +".color"
    ci = cmds.connectionInfo(cc,sfd=True)    
    if (ci=="") :
        ci = cmds.getAttr(cc)
        ci = ci[0]
        check = 0
    return (check, ci)    

# Check ramp attribute - shadow exist.
def rampCheck(name):
    check = 0
    crp = name+ ".colorRamp[0].colorRamp_Color"
    
    crp = cmds.getAttr(crp)
    if (crp[0] != (0.0,0.0,0.0) ) :
        check = 1
    return (check, crp[0])            
    
# Get shading group
def getSg(name):
    cOut = name+".outColor"
    sg = cmds.connectionInfo(cOut,dfs=True)
    return sg[0]

def toonRampControl(check, name):
    pos1 = name +".fbColorScale[3].fbColorScale_Position"
    pos2 = name +".fbColorScale[2].fbColorScale_Position"
    cmds.setAttr(pos1, 0.52)

    if check == 0 : num = 2
        
    if check == 1 : 
        num = 1
        cmds.setAttr(pos2, 0.48)
    
    for i in range(num):
        i = i+1
        cmds.removeMultiInstance(name+".fbColorScale["+str(i)+"]")



# Create Furryball Toon Material
def toonCreate(name, sg):
    cmds.delete(name)
    shd = cmds.shadingNode('furryballToonMaterial', asShader = True, n = name)
    cmds.connectAttr( name+".outColor", sg, f=True)
    return shd

# CONVERT 

mSels = cmds.ls(typ="MaroToonShader")

for x in mSels:
    cc = colorCheck(x)
    crp = rampCheck(x)
    sg = getSg(x)
    shd = toonCreate(x, sg)
    
    if (cc[0] == 1) :
        cmds.connectAttr(cc[1], shd+".color")
        
    else:
        cmds.setAttr(shd+".color", cc[1][0], cc[1][1], cc[1][2])
        cmds.setAttr(shd+".fbContourEnable", 0)

    cmds.setAttr(shd+".fbContourEnable", 0)
    cmds.setAttr(shd+".fbContourVariableWidth",1)
    cmds.setAttr(shd+".fbContourMinWidth",0.1)
    cmds.setAttr(shd+".fbContourMaxWidth", 2)
    cmds.setAttr(shd+".fbContourOverlabBias", 2)
    

    toonRampControl(crp[0],x)



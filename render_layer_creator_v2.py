# coding : euc-kr
# MARO render-layer creation script
#
# 2016.07.21
# ver 2.1
# by Musky

import maya.cmds as cmds
import maya.mel as mel
import types

cmds.setAttr("defaultResolution.width", 1920)
cmds.setAttr("defaultResolution.height", 1080)

def r_init(*args):
    open_file = 'file -import -type \"mayaBinary\" -ra true -mergeNamespacesOnClash false -namespace \"MI_LAYER_initialize\" -options \"v=0;\"  -pr \"Q:/MI/00_Guide/RenderPreset/MI_LAYER_initialize.mb\";\n'
    mel.eval(open_file)
    rls = cmds.ls(typ="renderLayer")
    rl = filter(lambda x:x !="defaultRenderLayer", rls)
    del_layer = ""
    for x in rl:
        mel.eval('editRenderLayerGlobals -currentRenderLayer defaultRenderLayer;')
        del_layer = 'delete ' + x +';\n'
        mel.eval(del_layer)

# SHADER Creator
def make_shd(name, rgb, t):

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
        cmds.setAttr(n+".outMatteOpacity",0,0,0,type='double3')

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
        cmds.setAttr(oc+".samples", 256)
        cmds.setAttr(oc+".max_distance", 25.0)
        cmds.setAttr(oc+".spread", 0.7)

    
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
        
        
  # MakeShader
    if not(cmds.objExists(s_name)): #Check that M_***_mat exists       
        cmds.shadingNode(s_type[t-1],n=s_name,asShader=True ) #Black_mat Shader Create
        cmds.sets(n=sg_name, renderable=True, noSurfaceShader=True, empty=True) #Set Shading Group
        cmds.connectAttr(s_name+".outColor", sg_name+".surfaceShader", f=True) #Connect shader to shading group
        
        if t == 1: set_color(s_name,rgb)
        if t == 2: set_shadow(s_name)         
        if t == 3: set_ao(s_name)
        if t == 4: set_depth(s_name)

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
        
#create light
def create_light(*args):

    light_name = args[0]
    if not(cmds.objExists(light_name)):
        # Create a directional light
        if args[1] == "dir":
            light = cmds.directionalLight( n=args[0],rotation=(-60, 5, 30))

            # Change the light intensity
            cmds.directionalLight( light, e=True, intensity=1 ,sc = (1,1,1), rs = 0)
            mel.eval( "setAttr " + light+".useDepthMapShadows 1;")
            mel.eval( "setAttr " + light+".dmapBias 10;")
            l_t = cmds.listRelatives(light, p=True)
            
        if args[1] == "pt":
            light = cmds.pointLight( n=args[0])
            cmds.pointLight (light, e=True, intensity = 1, rs=1)
            l_t = cmds.listRelatives(light, p=True)
            cmds.setAttr(l_t[0]+".ty", 20)
            
    return light_name

    

# Create Render Layer
def make_layer(name,sf,ef, r_type):
    rl_name = name
    sels = cmds.ls(sl=True)

    r_cam = cmds.textScrollList('r_cam', q=True, si=True)
    cs = lambda x:cmds.listRelatives(x,shapes=True)
    
    #check object exist
    if not(cmds.objExists(name)):
        l = cmds.createRenderLayer(n=rl_name, number=2,noRecurse=True)
        drg = "defaultRenderGlobals"
        
        cmds.editRenderLayerGlobals(crl=l)
        cmds.editRenderLayerAdjustment("defaultRenderGlobals.imageFilePrefix")
        cmds.editRenderLayerAdjustment("defaultRenderGlobals.imageFormat")
        cmds.editRenderLayerAdjustment(drg+".currentRenderer")
        cmds.setAttr(drg+".ren","mayaSoftware",typ="string")
        
        cmds.setAttr(drg+".imageFilePrefix",rl_name,typ="string")
        cmds.setAttr(drg+".imageFormat",32)
        cmds.setAttr(drg + ".startFrame", sf)
        cmds.setAttr(drg + ".endFrame", ef)

        put_obj(sels, rl_name)
        
    else: l = rl_name
    
    
    # Collect Camera data
    a_cam = cm_list()
    a_cam = a_cam[0]
    
    # All camera's renderable attribute is OFF.
    for ac in a_cam:
        cmds.setAttr(ac+".renderable", 0)
   
    # Turn on "renderble" : selected camera.
    if not(type(r_cam) == types.NoneType):
        for rc in r_cam:
            x = cs(rc)
            cmds.setAttr(x[0]+".renderable", 1)
    return l
    
# selected object -> render layer
def put_obj(obj,rl):
    if type(obj) == types.ListType:
        for x in obj:
            cmds.editRenderLayerMembers(rl,x,noRecurse=True)
    else :
        cmds.editRenderLayerMembers(rl,obj,noRecurse=True)
        

# render setting 
def maya_set(*args):
    # DF Maya Scanline render setting
    cmds.setAttr("defaultRenderQuality.edgeAntiAliasing",1)
    cmds.setAttr("defaultRenderQuality.shadingSamples",20)
    cmds.setAttr("defaultRenderQuality.useMultiPixelFilter",1)
    cmds.setAttr("defaultRenderQuality.pixelFilterType",2)
    cmds.setAttr("defaultRenderQuality.enableRaytracing",1)

def v_ray_set(*args):
    # NRM V-ray Setting
    cmds.setAttr("vraySettings.samplerType",1)
    cmds.setAttr("vraySettings.minShadeRate",2)
    cmds.setAttr("vraySettings.aaFilterOn",1)
    cmds.setAttr("vraySettings.aaFilterSize",1.5)
    cmds.setAttr("vraySettings.dmcMinSubdivs",1)
    cmds.setAttr("vraySettings.dmcMaxSubdivs",4)
    cmds.setAttr("vraySettings.giOn",0)
    mel.eval("vrayAddRenderElement normalsChannel;")

def mr_set(*args):
    # OC Mentalray Setting
    cmds.setAttr("miDefaultOptions.rayTracing",0)
    cmds.setAttr("miDefaultOptions.miRenderUsing",2)
    cmds.setAttr("miDefaultOptions.minSamples",1)
    cmds.setAttr("miDefaultOptions.maxSamples",4)
    cmds.setAttr("miDefaultOptions.contrastR",3)
    cmds.setAttr("miDefaultOptions.contrastG",3)
    cmds.setAttr("miDefaultOptions.contrastB",3)
    cmds.setAttr("miDefaultOptions.contrastA",3)
    cmds.setAttr("miDefaultOptions.filter",2)



        
        
# Get Render Layer Name
def get_name(t):
    
    name =  "EP_" + cmds.textFieldGrp('ep_field',q=True,text=True) +  "_SC" + cmds.textFieldGrp('sc_field',q=True,text=True) +  "_C"  + cmds.textFieldGrp('cn_field',q=True,text=True) +"_"   + cmds.textFieldGrp('ex_field',q=True,text=True) 
    cb = cmds.checkBox('c_box', q=True,  v=True)
    cus = cmds.textFieldGrp('cus', q=True, text=True)
 
    if cb : name = cus
    else  : name = name + "_" + t   

    return name

# button commands
def bRgb_mask(*args):
    t = "MASK"
    name = get_name(t)    
    sf = int(cmds.textFieldGrp('start_frame', q=True, tx=True))
    ef = int(cmds.textFieldGrp('end_frame', q=True, tx=True))
    print len(args)
    if args[0] == "char" :
        type_l = ("face", "hair", "all")
        for x in type_l:
            name = get_name(args[0]+"_"+x+"_"+t)
            make_layer(name,sf,ef,t)
    else: make_layer(name, sf, ef, t)
    
    rl = make_layer(name, sf, ef, t)
    cmds.editRenderLayerGlobals(crl= rl)
    cmds.setAttr("defaultRenderGlobals.ren", "mayaSoftware", typ='string')

    maya_set()
    return name
    
                 
def bNormal(*args):
    t = "NRM"
    if type(args[0]) == types.StringType:
        name = get_name(args[0]+"_"+t)  
    else : name = get_name(t)
    sf = int(cmds.textFieldGrp('start_frame', q=True, tx=True))
    ef = int(cmds.textFieldGrp('end_frame', q=True, tx=True))
    make_layer(name, sf, ef, t)    
    
    rl = make_layer(name, sf, ef, t)
    cmds.editRenderLayerGlobals(crl= rl)
    cmds.setAttr("defaultRenderGlobals.ren", "vray", typ='string')
    v_ray_set()
    
    return name
    
    
def bAO(*args):
    t = "AO"
    if type(args[0]) == types.StringType:
        name = get_name(args[0]+"_"+t)  
    else : name = get_name(t)
    sf = int(cmds.textFieldGrp('start_frame', q=True, tx=True))
    ef = int(cmds.textFieldGrp('end_frame', q=True, tx=True))
    
    rl = make_layer(name, sf, ef, t)
    cmds.editRenderLayerGlobals(crl= rl)
    cmds.setAttr("defaultRenderGlobals.ren", "mentalRay", typ='string')
    mr_set()
    
    m_override = 'hookShaderOverride(\"' +rl + '\", \"\", \"M_AO_mat\")'
    mel.eval(m_override)
    
    return name


def bZDepth(*args):
    t = "ZD"
    if type(args[0]) == types.StringType:
        name = get_name(args[0]+"_"+t)  
    else : name = get_name(t)    
    sf = int(cmds.textFieldGrp('start_frame', q=True, tx=True))
    ef = int(cmds.textFieldGrp('end_frame', q=True, tx=True))
    make_layer(name, sf, ef, t)    
    
    rl = make_layer(name, sf, ef, t)
    cmds.editRenderLayerGlobals(crl= rl)
    cmds.setAttr("defaultRenderGlobals.ren", "mayaSoftware", typ='string')

    maya_set()
    
    m_override = 'hookShaderOverride(\"' +rl + '\", \"\", \"M_zDepth_mat\")'
    mel.eval(m_override)

    return name
    
def bDiffuse(*args):
    t= "DF"
    if type(args[0]) == types.StringType:
        name = get_name(args[0]+"_"+t)  
    else : name = get_name(t)
    sf = int(cmds.textFieldGrp('start_frame', q=True, tx=True))
    ef = int(cmds.textFieldGrp('end_frame', q=True, tx=True))
    make_layer(name, sf, ef, t)   
    
    rl = make_layer(name, sf, ef, t)
    cmds.editRenderLayerGlobals(crl= rl)
    cmds.setAttr("defaultRenderGlobals.ren", "mayaSoftware", typ='string')

    maya_set()

    return name
    
def bShad(*args):
    t = "SHAD"
    if type(args[0]) == types.StringType:
        name = get_name(args[0]+"_"+t)  
    else : name = get_name(t)
    sf = int(cmds.textFieldGrp('start_frame', q=True, tx=True))
    ef = int(cmds.textFieldGrp('end_frame', q=True, tx=True))
    make_layer(name, sf, ef, t)   
    
    rl = make_layer(name, sf, ef, t)
    cmds.editRenderLayerGlobals(crl= rl)
    cmds.setAttr("defaultRenderGlobals.ren", "mayaSoftware", typ='string')

    maya_set()
    
    m_override = 'hookShaderOverride(\"' +rl + '\", \"\", \"M_Shadow_mat\")'
    mel.eval(m_override)
    
    return name
    
    
def bChar(*args):
    df = bDiffuse("char")
    bNormal("char")
    bRgb_mask("char")
    bZDepth("char")
    bAO("char")
    shad = bShad("char")
    c_lt = create_light("ch_light","dir")
    s_lt = create_light("shad_light","dir")
    put_obj(c_lt, df)
    put_obj(s_lt, shad)
    
def bBg(*args):
    df = bDiffuse("bg")
    bNormal("bg")
    bZDepth("bg")
    bAO("bg")
    b_lt = create_light("bg_light","pt")
    put_obj(b_lt,df)

# Get camera list // only perspective
def cm_list():
    cms = cmds.ls(typ='camera')
    cmt = lambda x:cmds.listRelatives(x,p=True)

    cm_list = filter(lambda x:not(cmds.getAttr(x+".orthographic")) , cms)
    cmt = cmt(cm_list)
    return (cm_list, cmt)
   


# Main GUI
def mrl_base_gui(*ars):
    gui = 'mrl_gui'
    
    if cmds.window(gui, q=1, ex=1):
        cmds.deleteUI(gui)

    cmds.window(gui,t="Render Layer Creator v2.0")
    shd_creation() # if default shader don't exist then create new shader.
    cmds.columnLayout(adjustableColumn = True)
    
    cmds.button('bInit', label= "Initialize", height = 25, bgc=(.4,.4,.7), c = r_init)
    
    cmds.text("Set Render Layer Name",align="center",h=25, bgc = (.3,.1,.1))
    cmds.textFieldGrp('ep_field', label='Episode',columnAlign=(1,'both'),columnWidth=(1,80))
    cmds.textFieldGrp('sc_field',label='Scene Number', columnAlign=(1,'both'),columnWidth=(1,80))
    cmds.textFieldGrp('cn_field', label='Cut Number', columnAlign=(1,'both'),columnWidth=(1,80))
    cmds.textFieldGrp('ex_field',label='Explanation',  columnAlign=(1,'both'),columnWidth=(1,80))
    cmds.checkBox('c_box', label = 'Use a custom name')
    cmds.textFieldGrp('cus',label='Custom',  columnAlign=(1,'both'),columnWidth=(1,80))
            
    sf = int(cmds.playbackOptions(q=True,ast=True))
    ef = int(cmds.playbackOptions(q=True,aet=True))
    cmds.text("Set Time Range",align="center",h=18, bgc = (.3,.1,.1))
    cmds.textFieldGrp('start_frame',label='Start Frame',tx = sf,columnAlign=(1,'both'),columnWidth=(1,80))  
    cmds.textFieldGrp('end frame', label='End Frame', tx = ef, columnAlign=(1,'both'),columnWidth=(1,80))
    cms = cm_list()
    cmds.text("Choose Render Camera",align="center",h=25, bgc = (.3,.1,.1))
    cmds.textScrollList('r_cam', append = cms[1],ams=True, h = 120)
    
    cmds.text("Create layer",align="center",h=22, bgc = (.3,.1,.1))
    cmds.rowColumnLayout(numberOfRows=2)
    cmds.button('diffuse', label= "DF", width=120,bgc=(.7,0.7,0.7), c=bDiffuse)
    cmds.button('normal', label= "NRM", width=120, bgc=(.7,0.7,0.7),c=bNormal)
    cmds.button('rgb_mask', label= "MASK", width=120,bgc=(.7,0.7,0.7), c=bRgb_mask)
    cmds.button('zDepth', label= "ZD", width=120,bgc=(.7,0.7,0.7), c=bZDepth)
    cmds.button('AO', label= "AO", width=120, bgc=(.7,0.7,0.7),c=bAO)
    cmds.button('shad', label= "SHAD", width=120, bgc=(.7,0.7,0.7),c=bShad)   
    cmds.setParent("..")
    cmds.rowColumnLayout(numberOfRows=1)
    cmds.button('a_char', label= "CHAR", width=180, bgc=(.9,0.8,0.7),c=bChar)    
    cmds.button('a_bg', label= "BG", width=180, bgc=(.9,0.8,0.7),c=bBg)    
    cmds.setParent("..")


    cmds.button( label ="Refresh",width=120,bgc=(0.3,.5,0.2), command=mrl_base_gui)
    
    cmds.window(gui, e=1, width=360, height = 120)
    cmds.showWindow(gui)


# GUI execute
mrl_base_gui()

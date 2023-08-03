import maya.cmds as mc
import re
# This script will auto-create 2-bone IK for the chain of the selected root joint

# For arms, True, True
# For legs, False, False
# User parameters
IK_controlSize = 3
# Whether the IK handle should reuse parent rotation axis
bParentControls = False
# Which way to move the pole vector handle
bPoleBack = False

# Switch params
switch_uniform_scale = 1.5
switch_dist = 10

# If true, will create pole vector for 2-bone IKs
# If false, will force all bone chains to use preferred angle
bCreatePole = True

def pack_selected_ctrl():
    sel_list = mc.ls(selection=1)
    for sel in sel_list:
        base_name = sel
        markers = ["_pri", "_sec", "_drv", "_con", "_ofs"]
        
        mc.select(sel)
        for i in range(0, 5):
            tgt = mc.ls(selection=1)[0]
            name = base_name+markers[i]
            mc.group(tgt, a=1, n=name)

cvTuples = {}
cvTuples['Locator'] = [
        (0.0, 2.001501540839854, 0.0),
        (0.0, -2.001501540839854, 0.0),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, -2.001501540839854),
        (0.0, 0.0, 2.001501540839854),
        (0.0, 0.0, 0.0),
        (2.001501540839854, 0.0, 0.0),
        (-2.001501540839854, 0.0, 0.0)
    ]
cvTuples['Box'] = [
        (-2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, -2.001501540839854, 2.001501540839854),
        (2.001501540839854, -2.001501540839854, 2.001501540839854),
        (2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, 2.001501540839854, -2.001501540839854),
        (-2.001501540839854, -2.001501540839854, -2.001501540839854),
        (-2.001501540839854, -2.001501540839854, 2.001501540839854),
        (2.001501540839854, -2.001501540839854, 2.001501540839854),
        (2.001501540839854, -2.001501540839854, -2.001501540839854),
        (2.001501540839854, 2.001501540839854, -2.001501540839854),
        (2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, 2.001501540839854, -2.001501540839854),
        (2.001501540839854, 2.001501540839854, -2.001501540839854),
        (2.001501540839854, -2.001501540839854, -2.001501540839854),
        (-2.001501540839854, -2.001501540839854, -2.001501540839854)
    ]
    
cvTuples['Cross Thin'] = [
        (-0.40030030816797085, 0.0, -2.001501540839854),
        (-0.40030030816797085, 0.0, -0.40030030816797085),
        (-2.001501540839854, 0.0, -0.40030030816797085),
        (-2.001501540839854, 0.0, 0.40030030816797085),
        (-0.40030030816797085, 0.0, 0.40030030816797085),
        (-0.40030030816797085, 0.0, 2.001501540839854),
        (0.40030030816797085, 0.0, 2.001501540839854),
        (0.40030030816797085, 0.0, 0.40030030816797085),
        (2.001501540839854, 0.0, 0.40030030816797085),
        (2.001501540839854, 0.0, -0.40030030816797085),
        (0.40030030816797085, 0.0, -0.40030030816797085),
        (0.40030030816797085, 0.0, -2.001501540839854),
        (-0.40030030816797085, 0.0, -2.001501540839854)
    ]

def bsDrawCurve(curve, thickness):
    crv = cmds.curve(d=1, p=cvTuples[curve])

    # Only adjusting the lineWidth attribute only if a value greater than 1.0 is input.
    if thickness > 1.0:
        crvShape = cmds.listRelatives(crv, s=True)
        for c in crvShape:
            cmds.setAttr('%s.lineWidth'%(c), thickness)
    else:
        pass

    return crv

def bsNameCurve(obj, name):
    # List of common suffixes to remove
    suffixList = ['_JNT','_Jnt','_jnt','_Bnd','_BND','_bnd','_JT','_Jt','_jt','_DRV','Drv','_drv','_CON','_Con','_con','_CTRL','_Ctrl','ctrl'
                        '_anim','_ANIM','_Anim','_LOC','_Loc','_loc','_GRP','_Grp','_grp']

    if name == '':
        newName = obj + '_ANIM' # Default suffix to add.
    else:
        if ' ' in name:
            newName = name.replace(' ', '_')
            newName = newName.split('_')
        else:
            newName = name.split('_')

        if len(newName) > 1:
            newName = '_'.join(newName)
        else:
            newName = obj
            for suf in suffixList:
                newName = newName.replace(suf, '')
            newName = newName + '_' + name

    return newName

def bsCurvePosition(obj, curve, thickness, name, parent):
    # Creating and naming curve.
    newName = bsNameCurve(obj, name)
    crv = bsDrawCurve(curve, thickness)
    crv = cmds.rename(crv, name)

    if parent:
        # Matching positions with a parent constraint.
        const = cmds.parentConstraint(obj, crv)
        cmds. delete(const)
    else:
        # Matching positions with a parent constraint.
        const = cmds.pointConstraint(obj, crv)
        cmds. delete(const)
    return crv

def list_all_children(nodes):
    """Fast, but slow when nesting is very deep."""
    
    result = set()
    children = set(mc.listRelatives(nodes) or [])
    while children:
        result.update(children)
        children = set(mc.listRelatives(children) or []) - result
        
    return list(result)


def create_switch_on_selected_roots():
    sel_list = mc.ls(selection=1)
    j_suffix_pack = ["Root_JNT", "Mid_JNT", "End_JNT"]
    j_IK = "IK"
    j_FK = "FK"
    j_BK = "Blend"

    prefix_pack = []

    valid = False
    for j in sel_list:
        mark = re.match(".*(?:FK|IK|Blend)Root_JNT", j)
        if mark:
            locator = re.search("(?:FK|IK|Blend)", j)
            print(locator)
            tmp_prefix = j[:locator.start()]
            if not tmp_prefix in prefix_pack:
                prefix_pack.append(tmp_prefix)
                valid = True
            
    if valid:
        # Create actual joint processors
        for j_prefix in prefix_pack:        
            # Create switch value controller at root of IK joint
            handle_name = j_prefix + "IK" + j_suffix_pack[0]
            control_name = j_prefix + "_switcher"
            bParentControls = True
            crv = bsCurvePosition(handle_name, 'Cross Thin', 1, control_name, bParentControls)
            
            mc.select(control_name)
            mc.setAttr(control_name+".scaleX", switch_uniform_scale)
            mc.setAttr(control_name+".scaleY", switch_uniform_scale)
            mc.setAttr(control_name+".scaleZ", switch_uniform_scale)
            mc.setAttr(control_name+".rotateX", 90)
            mc.setAttr(control_name+".rotateY", 0)
            mc.setAttr(control_name+".rotateZ", 0)
            
            # Move controller handle to side of root bone
            tmp_osPos = mc.xform(os=1, q=1, t=1)
            # 1 or -1, this indicates how to move controller handle further from world center
            tmp_dir = tmp_osPos[0] / abs(tmp_osPos[0])
            mc.xform(os=1, r=1, t=[tmp_dir * switch_dist, 0, 0])
            
            # We freeze only t and s, if freeze r, the pivot will change
            mc.makeIdentity(apply=True, t=1, r=0, s=1, n=0)
            pack_selected_ctrl()
            pack_root_name = control_name+"_ofs"
            mc.parent(pack_root_name, j_prefix + "Blend" + j_suffix_pack[0])
            
            # Fix controller rotation pivot value to 0 by adding fix transform node
            mc.select(control_name)
            mc.duplicate(control_name, rr=True)
            new_ctrl = mc.ls(selection=1)[0]
            mc.delete(new_ctrl + "Shape")
            mc.rename(control_name+"_fix")
            mc.parent(control_name, control_name+"_fix")
            mc.select(control_name+"_fix")
            
            mc.setAttr('%s.overrideEnabled'%(control_name), 1)
            mc.setAttr('%s.overrideColor'%(control_name), 6)
            #mc.parent(handle_name, control_name)
            mc.select(control_name)
            
            to_lock_attrs = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".v"]
            for att in to_lock_attrs:
                mc.setAttr(control_name + att, lock=1, keyable=0, channelBox=0)
            
            mc.addAttr(control_name, ln="IKFK_switch", at="double", min=0, max=10, dv=0)
            mc.setAttr(control_name + ".IKFK_switch", keyable=1)
            switch_out_plug = control_name + ".IKFK_switch"
            divider_name = control_name+"_divider"
            mc.createNode("multiplyDivide", n=divider_name)
            mc.connectAttr(switch_out_plug, divider_name+".input1X")
            mc.setAttr(divider_name+".input2X", 0.1)
            divider_plug = divider_name+".outputX"
            
            for i in range(0, 3):
                j_IK = j_prefix + "IK" + j_suffix_pack[i]
                j_FK = j_prefix + "FK" + j_suffix_pack[i]
                j_BK = j_prefix + "Blend" + j_suffix_pack[i]
                print(j_IK)
                print(j_FK)
                print(j_BK)
                blend_node = mc.createNode("blendColors", n=j_prefix+j_suffix_pack[i]+"_IKSwitch_BlendColors")
                mc.connectAttr(j_IK + ".rotate", blend_node + ".color1")
                mc.connectAttr(j_FK + ".rotate", blend_node + ".color2")
                mc.connectAttr(blend_node + ".output", j_BK+".rotate")
                mc.connectAttr(divider_plug, blend_node + ".blender")
                
    # TODO: Find wrist end bone and create controller
    # Then assign IKFK switch to the created controller
    else:
        print("IKFK switch creator: No valid joint selected, process aborted")

#Actual function
root_joints = mc.ls(selection=1)
for root_joint in root_joints:
    valid = False
    mc.select(root_joint)
    print(root_joint)
    mid_joint = ""
    end_joint = ""
    handle_name = root_joint[:-8]+"_HDL" # blahblahRoot_JNT - blahblah
    control_name = root_joint[:-8]+"_CTL"
    pole_name = root_joint[:-8]+"Pole_CTL"
    if(re.match(".*Root_JNT", root_joint)):
        child = list_all_children(root_joint)
        print(child)
        if len(child) == 2 and bCreatePole:
            # This is a standard 2-bone IK
            if re.match(".*Mid_JNT", child[0]) and re.match(".*End_JNT", child[1]):
                valid = True
                end_joint = child[1]
                mid_joint = child[0]
            elif re.match(".*Mid_JNT", child[1]) and re.match(".*End_JNT", child[0]):
                valid = True
                end_joint = child[0]
                mid_joint = child[1]
        elif (len(child) > 2 or not bCreatePole):
            # This is a long chain IK, hair, finger, etc
            # We use preferred angle as Pole vector, and do not create pole handle
            
            for ej in child:
                if re.match(".*End_JNT", ej):
                    end_joint = ej
            if end_joint == "":
                print("No end joint found, ABORTED.")
            
            # Select all chain joints
            mc.select(root_joint, r=1)
            for j in child:
                mc.select(j, add=1)
            print("Execute " + handle_name)
            mc.joint(e=1, spa=1)
            print("Execute " + handle_name)
            mc.ikHandle( n=handle_name, sj=root_joint, ee=end_joint)
            
            # Create Handle on end joint
            mc.select(end_joint, r=1)
            
            # TODO: Current only generate by parent joint rot
            #       Make a function that ignores parent joint rot
            crv = bsCurvePosition(end_joint, 'Box', 1, control_name, bParentControls)
            
            mc.select(control_name)
            mc.setAttr(control_name+".scaleX", control_uniform_scale)
            mc.setAttr(control_name+".scaleY", control_uniform_scale)
            mc.setAttr(control_name+".scaleZ", control_uniform_scale)
            
            # We freeze only t and s, if freeze r, the pivot will change
            mc.makeIdentity(apply=True, t=1, r=0, s=1, n=0)
            pack_selected_ctrl()
            
            # Fix controller rotation pivot value to 0 by adding fix transform node
            mc.select(control_name)
            mc.duplicate(control_name, rr=True)
            new_ctrl = mc.ls(selection=1)[0]
            mc.delete(new_ctrl + "Shape")
            mc.rename(control_name+"_fix")
            mc.parent(control_name, control_name+"_fix")
            mc.select(control_name+"_fix")
            
            mc.setAttr('%s.overrideEnabled'%(control_name), 1)
            mc.setAttr('%s.overrideColor'%(control_name), 13)
            mc.parent(handle_name, control_name)
            mc.select(control_name)
            
            # Create sub group of handle to later constraint wrist bone with.
            # Else the wrist bone won't follow IK Handle's rotation
            mc.select(handle_name, r=1)
            algnofst = mc.group(em=1, n=root_joint[:-8]+"AlignedOffset", p=handle_name)
            algn = mc.group(em=1, n=root_joint[:-8]+"Aligned", p=algnofst)
            mc.orientConstraint(algn, end_joint, mo=1)
            
            mc.select(root_joint, r=1)
            create_switch_on_selected_roots()
            
    if valid:
        # Create IK chain
        mc.ikHandle( n=handle_name, sj=root_joint, ee=end_joint)
        
        # Create Handle on end joint
        mc.select(end_joint, r=1)
        
        # TODO: Current only generate by parent joint rot
        #       Make a function that ignores parent joint rot
        crv = bsCurvePosition(end_joint, 'Box', 1, control_name, bParentControls)
        
        mc.select(control_name)
        mc.setAttr(control_name+".scaleX", control_uniform_scale)
        mc.setAttr(control_name+".scaleY", control_uniform_scale)
        mc.setAttr(control_name+".scaleZ", control_uniform_scale)
        
        # We freeze only t and s, if freeze r, the pivot will change
        mc.makeIdentity(apply=True, t=1, r=0, s=1, n=0)
        pack_selected_ctrl()
        
        # Fix controller rotation pivot value to 0 by adding fix transform node
        mc.select(control_name)
        mc.duplicate(control_name, rr=True)
        new_ctrl = mc.ls(selection=1)[0]
        mc.delete(new_ctrl + "Shape")
        mc.rename(control_name+"_fix")
        mc.parent(control_name, control_name+"_fix")
        mc.select(control_name+"_fix")
        
        mc.setAttr('%s.overrideEnabled'%(control_name), 1)
        mc.setAttr('%s.overrideColor'%(control_name), 13)
        mc.parent(handle_name, control_name)
        mc.select(control_name)
        
        # Create pole vector controller at mid joint with world pivot
        crv = bsCurvePosition(mid_joint, 'Locator', 1, pole_name, False)
        mc.setAttr('%s.overrideEnabled'%(pole_name), 1)
        mc.setAttr('%s.overrideColor'%(pole_name), 13)
        mc.setAttr(pole_name+".scaleX", IK_controlSize)
        mc.setAttr(pole_name+".scaleY", IK_controlSize)
        mc.setAttr(pole_name+".scaleZ", IK_controlSize)
        mc.makeIdentity(apply=True, t=1, r=0, s=1, n=0)
        pack_selected_ctrl()
        
        # Move the pole handle along the given plain created by the 2 bones
        # This way the Ik result won't change from it's origin
        
        # Find the direction of the ik plane
        root_w_pos = om.MVector(mc.xform(root_joint, q=True, ws=True, t=True))
        mid_w_pos = om.MVector(mc.xform(mid_joint, q=True, ws=True, t=True))
        end_w_pos = om.MVector(mc.xform(end_joint, q=True, ws=True, t=True))
        
        # Get distance and move handle
        pole_handle_diantance = 10
        ofst_v = (mid_w_pos - (root_w_pos+end_w_pos)/2).normal()*pole_handle_diantance
        mc.xform(crv, ws=True, t=ofst_v)
        
        # Bind pole handle
        mc.makeIdentity(apply=True, t=1, r=0, s=1, n=0)
        mc.poleVectorConstraint(crv, handle_name)
        
        # Create sub group of handle to later constraint wrist bone with.
        # Else the wrist bone won't follow IK Handle's rotation
        mc.select(handle_name, r=1)
        algnofst = mc.group(em=1, n=root_joint[:-8]+"AlignedOffset", p=handle_name)
        algn = mc.group(em=1, n=root_joint[:-8]+"Aligned", p=algnofst)
        mc.orientConstraint(algn, end_joint, mo=1)
        
        mc.select(root_joint, r=1)
        create_switch_on_selected_roots()
        
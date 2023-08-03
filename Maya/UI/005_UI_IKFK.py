import maya.cmds as mc
import re
import maya.api.OpenMaya as om

# The user is EXPECTED to group fingers of each hand/feet into groups, without connection to wrist / ankle joints

# This script will find all same-leveled joints and treat them all as fingers
# Selected root joints in different groups will be treated separatedly

# User may select root joints freely, it doesn't how many joints balonging to a certain hand is selected, it will always be processed
# DO NOT SELECT ANY JOINT YOU WISH NOT AS FINGER JOINTS

# Also, the fingers under each group should be in sequential order, from pinkey to thumb

import maya.cmds as mc
import re

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
    return base_name+markers[-1]

cvTuples = {}
cvTuples['Square'] = [
        (-2.001501540839854, 0.0, -2.001501540839854),
        (-2.001501540839854, 0.0, 2.001501540839854),
        (2.001501540839854, 0.0, 2.001501540839854),
        (2.001501540839854, 0.0, -2.001501540839854),
        (-2.001501540839854, 0.0, -2.001501540839854)
    ]
    
cvTuples['Circle Pin'] = [
        (0.0, 3.6012403205778734, 0.0),
        (-0.18778610161340414, 3.616019375585509, 0.0),
        (-0.3709482346983487, 3.659992707756567, 0.0),
        (-0.5449764638842179, 3.7320775476619334, 0.0),
        (-0.7055854499305741, 3.830498877526053, 0.0),
        (-0.8488206839113831, 3.952833291509765, 0.0),
        (-0.9711550978950942, 4.096068453940357, 0.0),
        (-1.069576499309432, 4.256677439986713, 0.0),
        (-1.1416613392147976, 4.430705633397475, 0.0),
        (-1.1856346713858557, 4.613867838032635, 0.0),
        (-1.2004137263934913, 4.801653760770498, 0.0),
        (-1.1856346713858557, 4.989439683508361, 0.0),
        (-1.1416613392147976, 5.172601888143522, 0.0),
        (-1.069576499309432, 5.3466300815542835, 0.0),
        (-0.9711550978950942, 5.507239067600639, 0.0),
        (-0.8488206839113831, 5.650474230031231, 0.0),
        (-0.7055854499305741, 5.772808644014942, 0.0),
        (-0.5449764638842179, 5.871229973879063, 0.0),
        (-0.3709482346983487, 5.943314813784429, 0.0),
        (-0.18778610161340414, 5.987288145955486, 0.0),
        (0.0, 6.002067200963123, 0.0),
        (0.1877860479507416, 5.987288145955486, 0.0),
        (0.370948163148132, 5.943314813784429, 0.0),
        (0.5449763207837844, 5.871229973879063, 0.0),
        (0.7055853068301408, 5.772808644014942, 0.0),
        (0.8488204692607332, 5.650474230031231, 0.0),
        (0.9711548832444443, 5.507239067600639, 0.0),
        (1.069576213108565, 5.3466300815542835, 0.0),
        (1.141661053013931, 5.172601888143522, 0.0),
        (1.1856343851849889, 4.989439683508361, 0.0),
        (1.2004134401926245, 4.801653760770498, 0.0),
        (1.1856343851849889, 4.613867838032635, 0.0),
        (1.141661053013931, 4.430705633397475, 0.0),
        (1.069576213108565, 4.256677439986713, 0.0),
        (0.9711548832444443, 4.096068453940357, 0.0),
        (0.8488204692607332, 3.952833291509765, 0.0),
        (0.7055853068301408, 3.830498877526053, 0.0),
        (0.5449763207837844, 3.7320775476619334, 0.0),
        (0.370948163148132, 3.659992707756567, 0.0),
        (0.1877860479507416, 3.616019375585509, 0.0),
        (0.0, 3.6012403205778734, 0.0),
        (0.0, 0.0, 0.0)
    ]

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
    if curve == 'Circle':
        crv = cmds.circle(d=3, r=2, nr=[0,1,0], ch=False)
    else: 
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

def create_clean_control(parent_name, control_name, color_theme=13, control_scale=1, dist_from_center=5, bParent=True, control_type='Square', init_rot=[0,0,0], blocked_attrs=[], bKeepRot=False):
    """
    @Param:
             parent_name: The name of the parent node this controller get's original transform from
            control_name: The name of this controller
             color_theme: The color of this controller
           control_scale: The original scale of this controller, note this scale will be frozen and the controller's terminal scale will be shown as 1
        dist_from_center: How far the controller should move from center, used mostly for major controls that separates from joints and hovers nearby
                 bParent: Whether this controller should be parented to the given parent
            control_type: The shape of this controller
                init_rot: Initial rotation of this controller, if bKeepRot is False, this is set directly to the attribute, else this is given as a local additive to the controller
           blocked_attrs: The attributes to be blocked and hidden on this controller
    """
    hdl_dist = dist_from_center
    bParentControls = bParent
    crv = bsCurvePosition(parent_name, control_type, 1, control_name, bParentControls)
    
    mc.select(control_name)
    mc.setAttr(control_name+".scaleX", control_scale)
    mc.setAttr(control_name+".scaleY", control_scale)
    mc.setAttr(control_name+".scaleZ", control_scale)
    if bKeepRot:
    # If keep rotation, rotation modifiers are added to local rot of generated controller
        mc.xform(os=1, r=1, ro=init_rot)
    else:
        mc.setAttr(control_name+".rotateX", init_rot[0])
        mc.setAttr(control_name+".rotateY", init_rot[1])
        mc.setAttr(control_name+".rotateZ", init_rot[2])
    
    # Move controller handle to side of root bone
    tmp_osPos = mc.xform(os=1, q=1, t=1)
    # 1 or -1, this indicates how to move controller handle further from world center
    if tmp_osPos[0] != 0:
        # TODO: What if joint is at world center
        tmp_dir = tmp_osPos[0] / abs(tmp_osPos[0])
    else:
        tmp_dir = 0
    mc.xform(os=1, r=1, t=[tmp_dir * hdl_dist, 0, 0])
    
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
    mc.setAttr('%s.overrideColor'%(control_name), color_theme)
    mc.select(control_name)
    
    for att in blocked_attrs:
        mc.setAttr(control_name + att, lock=1, keyable=0, channelBox=0)
    return control_name+"_ofs"
    
def list_all_children(nodes):
    """Fast, but slow when nesting is very deep."""
    
    result = set()
    children = set(mc.listRelatives(nodes) or [])
    while children:
        result.update(children)
        children = set(mc.listRelatives(children) or []) - result
        
    return list(result)

def executeFKChain(self):
    # TODO: Change from value link to transform reparent
    # Because we need to support FK transform & scale
    # Also, we need to blend not only rotation but also trans and scale in IK switch
    FK_controlSize = mc.floatSliderGrp(UI_FK_controlSize, query=True, value=True)
    bControlEndJoint = mc.checkBox(UI_bControlEndJoint, query=True, value=True)
    FK_root_pack = []
    sel_list = mc.ls(selection = 1)
    valid = False
    for j in sel_list:
        if re.match(".*Root_JNT", j):
            FK_root_pack.append(j)

    for p in FK_root_pack:
        # Get all chain children
        root_tmp = p
        parent_node = mc.listRelatives(p, parent=1)[0]
        chain_joints = mc.listRelatives(p, ad=1, typ="joint")
        chain_joints.append(root_tmp)
        chain_joints.reverse()
        if not bControlEndJoint:
            chain_joints.pop()
        print(chain_joints)
        prev_parent = parent_node
        rootFKcontrolName = chain_joints[0][:-4]+"FKcontrol"
        for cj in chain_joints:
            control_name = cj[:-4]+"FKcontrol"
            cj_ctrl = create_clean_control(cj, control_name, 18, FK_controlSize, 0, True, 'Circle', [0,0,0], ['.v'], True)
            
            # Create parent relationship between controller and FK bones
            mc.parent(cj_ctrl, prev_parent)
            prev_parent = control_name
            
            # TODO: Link control value to joint value without parenting
            # Because parented joint does not have values and can only transfer rotation by constraints
            mc.parentConstraint(control_name, cj, mo=1)
            mc.scaleConstraint(control_name, cj, mo=1)
        return rootFKcontrolName


def create_switch_on_selected_roots(packFK, IKControlPackage):
    # In IKControlPackage, the first is the ik handle, second (if valid) is the pole vector handle
    
    IKswitch_controlSize = mc.floatSliderGrp(ikf2, query=True, value=True)
    switch_dist = mc.floatSliderGrp(ikf3, query=True, value=True)
    
    sel_list = mc.ls(selection=1)
    # TODO: Make this list fit selecting chain
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
            mc.setAttr(control_name+".scaleX", IKswitch_controlSize)
            mc.setAttr(control_name+".scaleY", IKswitch_controlSize)
            mc.setAttr(control_name+".scaleZ", IKswitch_controlSize)
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
            joint_group = mc.listRelatives(j_prefix + "Blend" + j_suffix_pack[0], p=1)[0]
            mc.parent(pack_root_name, joint_group)
            
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
            switch_divider = mc.createNode("multiplyDivide", n=control_name+"_div")
            mc.setAttr(switch_divider+".input2X", 0.1)
            mc.connectAttr(switch_out_plug, switch_divider+".input1X")
            switch_out_plug = switch_divider+".outputX"
            
            
            # TODO: Change from math method to constraint weight method
            
            
            for i in range(0, 7):
                j_IK = j_prefix + "IK" + j_suffix_pack[i]
                j_FK = j_prefix + "FK" + j_suffix_pack[i]
                j_BK = j_prefix + "Blend" + j_suffix_pack[i]
                print(j_IK)
                print(j_FK)
                print(j_BK)
                
                # Because Constraint takes initial position as base, we need to make sure all three bones are now in the same position
                IK_pos = mc.xform(j_IK, ws=1, q=1, t=1)
                mc.xform(j_BK, ws=1, a=1, t=IK_pos)
                mc.xform(j_FK, ws=1, a=1, t=IK_pos)
                name_parentConst = j_prefix+j_suffix_pack[i]+"IKFKparentConst"
                name_scaleConst = j_prefix+j_suffix_pack[i]+"IKFKscaleConst"
                mc.parentConstraint(j_IK, j_BK, mo=0, n=name_parentConst, w=1)
                mc.parentConstraint(j_FK, j_BK, mo=0, n=name_parentConst, w=0)
                mc.scaleConstraint(j_IK, j_BK, mo=0, n=name_scaleConst, w=1)
                mc.scaleConstraint(j_FK, j_BK, mo=0, n=name_scaleConst, w=0)
                
                
                # This weight list is [IKWeight, FKWeight]
                parentConst_weightList = mc.parentConstraint(name_parentConst, q=1, wal=1)
                scaleConst_weightList = mc.scaleConstraint(name_scaleConst, q=1, wal=1)
                
                # Connect switch to constraint weight
                mc.connectAttr(switch_out_plug, name_parentConst+"."+parentConst_weightList[0])
                mc.connectAttr(switch_out_plug, name_scaleConst+"."+scaleConst_weightList[0])
                
                switch_rev=mc.createNode("reverse", n=control_name+"_rev")
                mc.connectAttr(switch_out_plug, switch_rev+".inputX")
                mc.connectAttr(switch_rev+".outputX", name_parentConst+"."+parentConst_weightList[1])
                mc.connectAttr(switch_rev+".outputX", name_scaleConst+"."+scaleConst_weightList[1])
                
        # Automating FK creation
        if packFK:
            mc.select(j_prefix + "FK" + j_suffix_pack[0] , r=1)
            rootFKcontrol = executeFKChain(0)
            # TODO: Connect visibility from switch to IKFK controllers
            switch_vis_rev = mc.createNode("reverse", n=j_prefix+"_switcher_vis_rev")
            mc.connectAttr(switch_divider+".outputX", switch_vis_rev+".inputX")
            switch_vis_mult = mc.createNode("multiplyDivide", n=j_prefix+"_switcher_vis_mult")
            mc.connectAttr(switch_vis_rev+".outputX", switch_vis_mult+".input1X")
            mc.connectAttr(switch_divider+".outputX", switch_vis_mult+".input1Y")
            mc.setAttr(switch_vis_mult+".input2X", 10)
            mc.setAttr(switch_vis_mult+".input2Y", 10)
            
            # TODO: unlock all visibilities
            mc.setAttr(rootFKcontrol+".visibility", lock=0)
            mc.connectAttr(switch_vis_mult+".outputX", rootFKcontrol+".visibility")
            for ikc in IKControlPackage:
                mc.setAttr(ikc+".visibility", lock=0)
                mc.connectAttr(switch_vis_mult+".outputY", ikc+".visibility")
        
    else:
        print("IKFK switch creator: No valid joint selected, process aborted")

def executeIKChain(self, packFK):
    IK_controlSize = mc.floatSliderGrp(ikf1, query=True, value=True)
    bCreatePole = mc.checkBox(ikcb1, query=True, value=True)
    bPoleBack = mc.checkBox(ikcb2, query=True, value=True)
    bParentControls = mc.checkBox(ikcb3, query=True, value=True)
    bCreateSwitchIfAble = mc.checkBox(ikcb4, query=True, value=True)
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
                # This package will give the switch the root group of the generated handle to toggle visibility
                IK_rootControl_package = []
                
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
                mc.setAttr(control_name+".scaleX", IK_controlSize)
                mc.setAttr(control_name+".scaleY", IK_controlSize)
                mc.setAttr(control_name+".scaleZ", IK_controlSize)
                
                # We freeze only t and s, if freeze r, the pivot will change
                mc.makeIdentity(apply=True, t=1, r=0, s=1, n=0)
                IK_rootControl_package.append(pack_selected_ctrl())
                
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
                if bCreateSwitchIfAble:
                    create_switch_on_selected_roots(packFK, IK_rootControl_package)
            else:
                print("Invalid IK chain type, aborted\nCheck if chain is 2-bone IK")
                
        if valid:
            # This package will give the switch the root group of the generated handle to toggle visibility
            IK_rootControl_package = []
            # Create IK chain
            mc.ikHandle( n=handle_name, sj=root_joint, ee=end_joint)
            
            # Create Handle on end joint
            mc.select(end_joint, r=1)
            
            # TODO: Current only generate by parent joint rot
            #       Make a function that ignores parent joint rot
            crv = bsCurvePosition(end_joint, 'Box', 1, control_name, bParentControls)
            
            mc.select(control_name)
            mc.setAttr(control_name+".scaleX", IK_controlSize)
            mc.setAttr(control_name+".scaleY", IK_controlSize)
            mc.setAttr(control_name+".scaleZ", IK_controlSize)
            
            # We freeze only t and s, if freeze r, the pivot will change
            mc.makeIdentity(apply=True, t=1, r=0, s=1, n=0)
            tmp = pack_selected_ctrl()
            IK_rootControl_package.append(tmp)
            
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
            tmp = pack_selected_ctrl()
            IK_rootControl_package.append(tmp)
            
            # Move the pole handle along the given plain created by the 2 bones
            # This way the Ik result won't change from it's origin
            
            # Find the direction of the ik plane
            root_w_pos = om.MVector(mc.xform(root_joint, q=True, ws=True, t=True))
            mid_w_pos = om.MVector(mc.xform(mid_joint, q=True, ws=True, t=True))
            end_w_pos = om.MVector(mc.xform(end_joint, q=True, ws=True, t=True))
            
            # Get distance and move handle
            pole_handle_distance = mc.floatSliderGrp(ikf4, query=True, value=True)
            ofst_v = (mid_w_pos - (root_w_pos+end_w_pos)/2).normal()*pole_handle_distance
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
            if bCreateSwitchIfAble:
                create_switch_on_selected_roots(packFK, IK_rootControl_package)

def executeIKChainPack(self):
    executeIKChain(self, packFK=True)
    
def executeIKChainOnly(self):
    executeIKChain(self, packFK=False)

window = mc.window(title="RIG_005 - IKFK Chain", width=300)

mainLayout = mc.columnLayout(adjustableColumn=True)

# Add elements row by row 
mc.text(label='FK Chain')
UI_bControlEndJoint = mc.checkBox(label='ControlEndJoint', value=True)
UI_FK_controlSize = mc.floatSliderGrp( label='FK ControlSize', field=True,  minValue=0, maxValue=10.0, value=3)
mc.button(label='Create only FK Chain', command=executeFKChain)

mc.text(label='\nIK Chain\nThe switch will be auto created if FK and blend joints are found')
ikcb1 = mc.checkBox(label='Create Pole-vector', value=True)
ikcb2 = mc.checkBox(label='Reverse pole-vector direction (No effect if not 2 bone)', value=False)
ikcb3 = mc.checkBox(label='IK handle follow end joint rotation', value=True)
ikcb4 = mc.checkBox(label='Create switch if able', value=True)
ikf1 = mc.floatSliderGrp( label='IK ControlSize', field=True,  minValue=0, maxValue=10.0, value=3)
ikf2 = mc.floatSliderGrp( label='Switch ControlSize', field=True,  minValue=0, maxValue=10.0, value=3)
ikf3 = mc.floatSliderGrp( label='Switch distance from center', field=True,  minValue=0, maxValue=100.0, value=10)
ikf4 = mc.floatSliderGrp( label='PoleHandle distance from mid', field=True,  minValue=0, maxValue=100.0, value=20)

mc.button(label='Create FK/IK Chain (Force switch creation)', command=executeIKChainPack)
mc.button(label='Create IK Chain only', command=executeIKChainOnly)


# Show window
mc.showWindow(window)
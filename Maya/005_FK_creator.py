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

FK_controlSize = 3
bControlEndJoint = True

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
    for cj in chain_joints:
        control_name = cj+"NameTest"
        cj_ctrl = create_clean_control(cj, control_name, 18, FK_controlSize, 0, True, 'Circle', [0,0,0], ['.v', '.tx', '.ty', '.tz'], True)
        
        # Create parent relationship between controller and FK bones
        mc.parent(cj_ctrl, prev_parent)
        prev_parent = control_name
        
        # TODO: Link control value to joint value without parenting
        # Because parented joint does not have values and can only transfer rotation by constraints
        mc.connectAttr(control_name+".rotate", cj+".rotate")


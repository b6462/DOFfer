import maya.cmds as mc
import maya.api.OpenMaya as om
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

foot_joints = []

print("=====Validating foot structure=====")
sel_list = mc.ls(selection=1)
for s in sel_list:
    if(re.match(".*Root_JNT", s)):
        # Check sublevel joint structure
        child_j_0 = mc.listRelatives(s, c=1)
        mid_match = False
        heel_match = False
        for c in child_j_0:
            if re.match(".*Mid_JNT", c):
                mid_match = c
            if re.match(".*Heel_JNT", c):
                heel_match = c
        if mid_match and heel_match:
            end_match = mc.listRelatives(mid_match, c=1)[0]
            if re.match(".*End_JNT", end_match):
                foot_joints.append([s, mid_match, end_match, heel_match])
print("=====Validation complete=====")

# Adjust size of target control uniformally
control_expansion_ratio = 0.8

if len(foot_joints)>0:
    print("Found foot joints: ")
    for f in foot_joints:
        print(f)
        j_root = f[0]
        j_mid = f[1]
        j_end = f[2]
        j_heel = f[3]
        j_prefix = j_root[:-8]
        print(j_prefix)
        
        # Get length of foot joint structure
        p_root = om.MVector(mc.xform(j_root, q=1, t=1, ws=1))
        p_heel = om.MVector(mc.xform(j_heel, q=1, t=1, ws=1))
        p_mid = om.MVector(mc.xform(j_mid, q=1, t=1, ws=1))
        p_end = om.MVector(mc.xform(j_end, q=1, t=1, ws=1))
        length_ctrl = (p_root - p_heel).length()*control_expansion_ratio
        # Normally the feet length-to-width ratio is 2~3:1
        width_ctrl = length_ctrl*0.4
        
        foot_grp = mc.listRelatives(j_root, p=1)[0]
        name_prefix = foot_grp[:-4]
        major_ctrl = name_prefix + "Major_CTL"
        
        
        major_ctrl_ofs = create_clean_control(j_heel, major_ctrl, 18, 1, 0, True, 'Square', [0,0,0], ['.v'], False)
        mc.parent(major_ctrl_ofs, foot_grp)
        mc.setAttr(major_ctrl+".sx", width_ctrl)
        mc.setAttr(major_ctrl+".sz", length_ctrl)
        
        # Move major ctl to center of end & heel
        tmp = mc.pointConstraint(j_heel, j_end, major_ctrl)
        mc.delete(tmp)
        
        # Add attributes to major control
        toAddList = ["heelRoll", "ballRoll", "toeRoll", "toeBend", "rock"]
        for ta in toAddList:
            mc.addAttr(major_ctrl, ln=ta, dv=0, at="double")
            mc.setAttr(major_ctrl+"."+ta, e=1, keyable=1)
        
        # Move major ctrl pivot to foot root
        p_pvt = om.MVector(mc.xform(major_ctrl+".rotatePivot", t=1, ws=1, q=1))
        p_pvt_delta = p_root - p_pvt
        mc.move(p_pvt_delta[0], p_pvt_delta[1], p_pvt_delta[2], major_ctrl+".scalePivot", major_ctrl+".rotatePivot", r=1)
        
        # TODO: This parent() will create a unwanted transform node above the joint
        mc.parent(j_root, major_ctrl)
        
        def move_pvt_to(pivot_to_move, target):
            p_pvt = om.MVector(mc.xform(pivot_to_move+".rotatePivot", t=1, ws=1, q=1))
            p_tgt = om.MVector(mc.xform(target, t=1, ws=1, q=1))
            p_pvt_delta = p_tgt - p_pvt
            mc.move(p_pvt_delta[0], p_pvt_delta[1], p_pvt_delta[2], pivot_to_move+".scalePivot", pivot_to_move+".rotatePivot", r=1)
            return pivot_to_move
        
        def pack_pivot_grp(child_j, parent_j, name, pivot_joint):
            pivot_group = mc.group(child_j, p=parent_j, n=name)
            p_pvt = om.MVector(mc.xform(pivot_group+".rotatePivot", t=1, ws=1, q=1))
            p_tgt = om.MVector(mc.xform(pivot_joint, t=1, ws=1, q=1))
            p_pvt_delta = p_tgt - p_pvt
            mc.move(p_pvt_delta[0], p_pvt_delta[1], p_pvt_delta[2], pivot_group+".scalePivot", pivot_group+".rotatePivot", r=1)
            return pivot_group
            
        
        # Create groups for each attr and set each pivot
        g_ballCounter = pack_pivot_grp(j_mid, j_root, j_prefix+"BallCounter_GRP", j_mid)
        g_toeRoll = pack_pivot_grp(major_ctrl_ofs, foot_grp, j_prefix+"ToeRoll_GRP", j_end)
        g_ballRoll = pack_pivot_grp(major_ctrl_ofs, g_toeRoll, j_prefix+"BallRoll_GRP", j_mid)
        g_heelRoll = pack_pivot_grp(major_ctrl_ofs, g_ballRoll, j_prefix+"HeelRoll_GRP", j_heel)
        g_rockIn = pack_pivot_grp(major_ctrl_ofs, g_heelRoll, j_prefix+"RockIn_GRP", j_end)
        g_rockOut = pack_pivot_grp(major_ctrl_ofs, g_rockIn, j_prefix+"RockOut_GRP", j_end)
        
        # Set Rocker pivots to edge of major controller
        
        # Find which is closer to 0,0,0, it will be set to inner
        p_cv0 = om.MVector(mc.xform(major_ctrl+".cv[0]", t=1, ws=1, q=1))
        p_cv3 = om.MVector(mc.xform(major_ctrl+".cv[3]", t=1, ws=1, q=1))
        if p_cv0.length()<p_cv3.length():
            move_pvt_to(g_rockIn, major_ctrl+".cv[0]")
            move_pvt_to(g_rockOut, major_ctrl+".cv[3]")
        else:
            move_pvt_to(g_rockIn, major_ctrl+".cv[3]")
            move_pvt_to(g_rockOut, major_ctrl+".cv[0]")
        
        # TODO: Link all new attr to groups
        mc.connectAttr(major_ctrl+".toeRoll", g_toeRoll+".rx")
        mc.connectAttr(major_ctrl+".heelRoll", g_heelRoll+".rx")
        mc.connectAttr(major_ctrl+".ballRoll", g_ballRoll+".rx")
        
        ball_adder = mc.createNode("plusMinusAverage", n=name_prefix+"Ball_add")
        ball_mult = mc.createNode("multiplyDivide", n=name_prefix+"Ball_mult")
        mc.connectAttr(ball_adder+".output3Dx", g_ballCounter+".rx")
        mc.connectAttr(major_ctrl+".toeBend", ball_adder+".input3D[0].input3Dx")
        mc.connectAttr(ball_mult+".outputX", ball_adder+".input3D[1].input3Dx")
        mc.setAttr(ball_mult+".input2X", -1)
        mc.connectAttr(major_ctrl+".ballRoll", ball_mult+".input1X")
        
        rockIn_clamp = mc.createNode("clamp", n=name_prefix+"rockIn_clamp")
        rockOut_clamp = mc.createNode("clamp", n=name_prefix+"rockOut_clamp")
        
        if p_cv0.length()<p_cv3.length():
            mc.setAttr(rockIn_clamp+".maxR", 180)
            mc.setAttr(rockOut_clamp+".minR", -180)
            mc.connectAttr(major_ctrl+".rock", rockIn_clamp+".inputR")
            mc.connectAttr(major_ctrl+".rock", rockOut_clamp+".inputR")
            mc.connectAttr(rockIn_clamp+".outputR", g_rockIn+".rz")
            mc.connectAttr(rockOut_clamp+".outputR", g_rockOut+".rz")
        else:
            # Reverse the rock value input to each rock GRP
            mc.setAttr(rockIn_clamp+".minR", -180)
            mc.setAttr(rockOut_clamp+".maxR", 180)
            rev_major_mult = mc.createNode("multiplyDivide", n=name_prefix+"ReverseMajor_mult")
            mc.connectAttr(major_ctrl+".rock", rev_major_mult+".input1X")
            mc.setAttr(rev_major_mult+".input2X", -1)
            mc.connectAttr(rev_major_mult+".outputX", rockIn_clamp+".inputR")
            mc.connectAttr(rev_major_mult+".outputX", rockOut_clamp+".inputR")
            mc.connectAttr(rockIn_clamp+".outputR", g_rockIn+".rz")
            mc.connectAttr(rockOut_clamp+".outputR", g_rockOut+".rz")
        
        
        mc.makeIdentity(major_ctrl, apply=True, t=1, r=0, s=1, n=0)
        
        # TODO: Make rock rotation mirror between L/R foot
else:
    print("No valid foot joint structure found")
    
import maya.cmds as mc

# The user is EXPECTED to group fingers of each hand/feet into groups, without connection to wrist / ankle joints
# Also, the fingers under each group should be in sequential order, from pinkey to thumb

# This script will find all same-leveled joints and treat them all as fingers
# Selected root joints in different groups will be treated separatedly

# User may select root joints freely, it doesn't how many joints balonging to a certain hand is selected, it will always be processed
# DO NOT SELECT ANY JOINT YOU WISH NOT AS FINGER JOINTS

import maya.cmds as mc
import re

def locator_on_joint(tgt_jnt, bFollowRot=True, bVisibility=False):
    mc.select(tgt_jnt)
    t_tgt = mc.xform(q=1, t=1, ws=1)
    print(t_tgt)
    r_tgt = mc.xform(q=1, ro=1, ws=1)
    print(r_tgt)
    
    tmp_loc_shape = mc.createNode("locator", n=tgt_jnt+"_LocShape")
    tmp_loc = mc.listRelatives(tmp_loc_shape, p=1)[0]
    
    mc.rename(tmp_loc, tgt_jnt+"_Loc")
    
    mc.select(tmp_loc, r=1)
    mc.move(t_tgt[0], t_tgt[1], t_tgt[2])
    mc.makeIdentity(tmp_loc, apply=True, t=1, r=0, s=1, n=0)
    
    if bFollowRot:
        mc.rotate(r_tgt[0], r_tgt[1], r_tgt[2])
        
        # Fix controller rotation pivot value to 0 by adding fix transform node
        mc.select(tmp_loc)
        mc.duplicate(tmp_loc, rr=True)
        new_ctrl = mc.ls(selection=1)[0]
        mc.delete(new_ctrl + "Shape")
        mc.rename(tmp_loc+"_fix")
        mc.parent(tmp_loc, tmp_loc+"_fix")
        mc.select(tmp_loc+"_fix")
    
    mc.setAttr(tmp_loc_shape+".visibility", bVisibility)
    
    return tmp_loc

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
    control_uniform_scale = control_scale
    hdl_dist = dist_from_center
    bParentControls = bParent
    crv = bsCurvePosition(parent_name, control_type, 1, control_name, bParentControls)
    
    mc.select(control_name)
    mc.setAttr(control_name+".scaleX", control_uniform_scale)
    mc.setAttr(control_name+".scaleY", control_uniform_scale)
    mc.setAttr(control_name+".scaleZ", control_uniform_scale)
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
    tmp_dir = tmp_osPos[0] / abs(tmp_osPos[0])
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
    


def create_fingers(*args):
    finger_type_pack = []
    sel_list = mc.ls(selection = 1)
    valid = False
    print("=====Validating selections=====\n")
    for j in sel_list:
        mark = re.match(".*Root_JNT", j)
        if mark:
            # Check if selected root is already contained
            redundant = False
            for ftp in finger_type_pack:
                if redundant:
                    break
                for fgr in ftp:
                    if redundant:
                        break
                    if j == fgr:
                        print("Joint " + j + " is already contained, passed as redundancy")
                        redundant = True
            if redundant:
                continue
            # If not contained, this is a root joint of a new finger group
            tmp_group = []
            print("Found root on " + j + ", validating fingers:")
            valid = True
            # Since this is a root joint, find it's parent group
            # And collect all children, they must all be fingers
            # We can then acquire namings of all fingers
            parent_node = mc.listRelatives(j, parent=1)[0]
            finger_nodes = mc.listRelatives(parent_node, children=1)
            for fig in finger_nodes:
                locator = re.search("Root_JNT", fig)
                tmp_prefix = fig[:locator.start()]
                tmp_group.append(tmp_prefix + "Root_JNT")
            finger_type_pack.append(tmp_group)
            print(tmp_group)

    print("\n=====Validation complete=====\n")        

    if valid:
        # Create FK system
        for ftp in finger_type_pack:
            # For each finger group, a mejor control is created to control all bendings
            major_control_scale = 5
            major_control_dist = 15
            major_group = mc.listRelatives(ftp[0], parent=1)[0]
            tmp_prefix = major_group[:-4]+"_Major"
            major_control_name = tmp_prefix+"_CTL"
            major_control_group_name = tmp_prefix+"Base_GRP"
            major_base = create_clean_control(major_group, major_control_group_name, 13, 0.5, major_control_dist, True, 'Square', [0,0,0], ['.v'])
            mc.parent(major_base, major_group)
            major_ctrl = create_clean_control(major_base, major_control_name, 17, 0.1, 0, True, 'Square', [0,0,0], ['.v', '.ty', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz'])
            mc.parent(major_ctrl, major_control_group_name)
            mc.aliasAttr("roll", major_control_name+'.tx')
            mc.aliasAttr("spread", major_control_name+'.tz')
            mc.transformLimits(major_control_name, etx=(1,1), etz=(1,1))
            
            # We only scale the whole control after it's creation, because we need to limit the controller's moving margin within the base
            mc.setAttr(major_control_group_name+".sx", major_control_scale)
            mc.setAttr(major_control_group_name+".sz", major_control_scale)
            
            # Create roll multiplier to map +-1 to +-90
            major_Roll_mult = mc.createNode('multiplyDivide', n=major_control_group_name+"_rollMult")
            mc.setAttr(major_Roll_mult+".input2X", 90)
            mc.connectAttr(major_control_name+".tx", major_Roll_mult+".input1X")
            
            majorSpread_mult_arr = []
            spreadMult_counter = 0
            
            for fgr in ftp:
                # Create the spread multiplier for this finger, 20 10 0 -10 -20 difference
                spreadMult_tmp = mc.createNode('multiplyDivide', n=fgr[:-8]+"_spreadMult")
                majorSpread_mult_arr.append(spreadMult_tmp)
                mc.setAttr(spreadMult_tmp+".input2X", 20-10*spreadMult_counter)
                mc.connectAttr(major_control_name+".tz", spreadMult_tmp+".input1X")
                spreadMult_counter += 1
            
                # Find all children of this finger joint
                fgr_chain = mc.listRelatives(fgr, ad=1)
                fgr_chain.append(fgr)
                fgr_chain.reverse()
                # Remove finger tip
                fgr_chain.pop()
                #['l_ringRoot_JNT', 'l_ringMid_JNT', 'l_ringTip_JNT'] 
                # NOTE there is no 'l_ringEnd_JNT'
                
                # Create semi-major controller on root joint
                rootMajorController = fgr[:-8]+"RootMajor_CTL"
                rootController = create_clean_control(fgr, rootMajorController, 17, 1, 0, True, 'Square', [180,180,90], ['.v'], True)
                mc.parent(rootController, major_group)
                # Connect spread value to root joint
                major_spread_add = mc.createNode('floatMath', n=fgr[:-4]+"_majorsemi_spread_adder")
                mc.connectAttr(spreadMult_tmp+".outputX", major_spread_add+".floatA")
                mc.connectAttr(rootMajorController+".rz", major_spread_add+".floatB")
                mc.connectAttr(major_spread_add+".outFloat", fgr+".rz")
                
                # For each finger in group, create a chain of FK controls
                prev_ctrl = major_group
                for f in fgr_chain:
                    jointController = f[:-4]+"_CTL"
                    tmp_chain_seg = create_clean_control(f, jointController, 18, 1, 0, True, 'Circle', [0,0,0], ['.v', '.tx', '.ty', '.tz'], True)
                    if prev_ctrl != "":
                        mc.parent(tmp_chain_seg, prev_ctrl)
                    prev_ctrl = f[:-4]+"_CTL"
                    
                    # Create intake nodes for each finger joints, as each joint will receive combination of three sets of controllers
                    fksemi_Roll_add = mc.createNode('floatMath', n=f[:-4]+"_fksemi_Roll_adder")
                    major_Roll_add = mc.createNode('floatMath', n=f[:-4]+"_major_Roll_adder")
                    
                    mc.connectAttr(major_Roll_mult+".outputX", fksemi_Roll_add+".floatA")
                    mc.connectAttr(rootMajorController+".ry", fksemi_Roll_add+".floatB")
                    mc.connectAttr(fksemi_Roll_add+".outFloat", major_Roll_add+".floatA")
                    
                    
                    mc.connectAttr(jointController+".rx", major_Roll_add+".floatB")
                    
                    mc.connectAttr(major_Roll_add+".outFloat", f+".rx")
                    
                    # The locator copys only rotation result of 2 major ctrls, adding to the fk control
                    # This is to avoid double transform
                    
                    fk_rot_locator = locator_on_joint(f)
                    mc.connectAttr(fksemi_Roll_add+".outFloat", fk_rot_locator+".rx")
                    mc.pointConstraint(f, fk_rot_locator, mo=1)
                    mc.parent(fk_rot_locator+"_fix", jointController+"_con")
                    mc.parent(jointController+"_drv", fk_rot_locator)
                    
        # TODO: Create IK system?
        # To do this we will have to create 3 sets of finger joint chains, like the arms & legs
    else:
        print("No valid root joint selected, operation aborted")



def create_foot(*args):
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


def create_rig006_window():
    if mc.window("RIG_006_window", exists=True):
        mc.deleteUI("RIG_006_window", window=True)
    
    window = mc.window("RIG_006_window", title="RIG_006 - Finger & Foot", widthHeight=(250, 150))
    mc.columnLayout(adjustableColumn=True)
    mc.text(label="RIG_006 - Finger & Foot", align="center", font="boldLabelFont", height=30)

    mc.button(label="Create finger rig", command=create_fingers)
    mc.button(label="Create foot rig", command=create_foot)

    mc.showWindow(window)

create_rig006_window()
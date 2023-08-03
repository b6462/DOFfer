# Given a curve and num of spine joints, this script creates attached spine joints upon the curve
# They are switchable between parented joint-chain & editable motion-path joints
import maya.cmds as mc

num_joints = 9
name_spine = "TestSpine"

curve = mc.listRelatives(mc.ls(selection=1)[0], ad=1)[0]

if mc.objectType(curve) == "nurbsCurve":
    for j in range(0, num_joints):
        tmp_joint = mc.createNode("joint", n=name_spine+str(j)+"_JNT")
        tmp_curveInfo = mc.createNode("pointOnCurveInfo", n=name_spine+str(j)+"_crvInfo")
        mc.connectAttr(curve+".worldSpace", tmp_curveInfo+".inputCurve")
        mc.connectAttr(tmp_curveInfo+".position", tmp_joint+".translate")
        mc.setAttr(tmp_curveInfo+".parameter", j/(num_joints-1))
        mc.setAttr(tmp_curveInfo+".turnOnPercentage", 1)
else:
    print("Invalid curve type, ABORTED") 

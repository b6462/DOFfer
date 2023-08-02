import maya.cmds as mc

# NOTE: This script is to be run after full boneChain naming Fixed
# NOTE: This script also assumes joint name sigularity, so no duplicate names

# This script will check each joint root by name
# And assigne according joint orient fix to it and it's child

# This part will show/hide orient axies
visualize_orient = 0
joint_list = mc.ls("*_JNT")
for j in joint_list:
    mc.setAttr(j+".displayLocalAxis", visualize_orient)

template = {
    "spine" : ["yxz", "xup"],
    "neck" : ["yxz", "xup"],
    "head" : ["yxz", "xup"],
    "arm" : ["yxz", "yup"],
    "index" : ["yxz", "zup"],
    "middle" : ["yxz", "zup"],
    "ring" : ["yxz", "zup"],
    "pinky" : ["yxz", "zup"],
    "thumb" : ["yxz", "xup"],
    "leg" : ["yxz", "xup"],
    "foot" : ["yxz", "xup"],
    "butt" : ["yxz", "xup"],
    "breast" : ["yxz", "xdown"],
}

root_list = mc.ls("*Root_JNT")
for j in root_list:
    # Check if singular
    mc.select(j)
    tmp_list = mc.listRelatives(ad=1, f=1)
    if len(tmp_list)==0:
        print("Singular joint, abort")
        pass
    tmp_type = j.split("_")[1][:-4]
    tplt = template[tmp_type]
    if tplt:
        print("Fixing " + j + "as type: " + tmp_type)
        print("Template" + str(tplt))
        mc.joint(edit=1, oj=tplt[0], sao=tplt[1], ch=1, zso=1)
        j.replace("Root_", "End_")
        tmp_split = j.split("_")
        nj = tmp_split[0] + "_" + tmp_type + "End_JNT"
        mc.select(nj)
        mc.joint(edit=1, oj="none", ch=1, zso=1)
    
    
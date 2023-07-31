# NOTE: This script is to be run after full boneChain naming Fixed
# NOTE: This script also assumes joint name sigularity, so no duplicate names

# This script will check each joint root by name
# And assigne according joint orient fix to it and it's child
# No selection is required

import maya.cmds as mc

def showOrient(self):
    joint_list = mc.ls("*_JNT")
    for j in joint_list:
        mc.setAttr(j+".displayLocalAxis", 1)

def hideOrient(self):
    joint_list = mc.ls("*_JNT")
    for j in joint_list:
        mc.setAttr(j+".displayLocalAxis", 0)

def execute_orientFix(self):
    template = {
        "spine" : ["yxz", "xup"],
        "neck" : ["yxz", "xup"],
        "head" : ["yxz", "xup"],
        "arm" : ["yxz", "yup"],
        "index" : ["yxz", "zup"],
        "middle" : ["yxz", "zup"],
        "ring" : ["yxz", "zup"],
        "pinky" : ["yxz", "zup"],
        "thumb" : ["yxz", "ydown"],
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

window = mc.window(title="RIG_002 - Fix Orient")  
form = mc.formLayout(numberOfDivisions=100)
title = mc.text(label='RIG_002 - Fix Orient')  
b1 = mc.button(label='Show Orient', command=showOrient)
b2 = mc.button(label='Hide Orient', command=hideOrient)
b3 = mc.button(label='Execute', command=execute_orientFix)

mc.formLayout( form, edit=True, 
    attachForm=[
        (title, 'top', 5), 
        (title, 'left', 5), 
        (b1, 'top', 5), 
        (b1, 'left', 5), 
        (b2, 'top', 5), 
        (b2, 'right', 5),
        (b3, 'left', 5), 
        (b3, 'bottom', 5), 
        (b3, 'right', 5)
    ],
    attachControl=[
        (b3, 'top', 5, b1),
        (b1, 'top', 5, title),
        (b2, 'top', 5, title),
    ],
    attachPosition=[
        (b1, 'right', 5, 50),
        (b2, 'left', 5, 50)
    ]
)

mc.showWindow( window )
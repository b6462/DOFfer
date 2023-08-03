import maya.cmds as mc

# This script aims to name bone chains automatically
# Root
# Root End
# Root Mid End
# Root Mid Tip End
# Root spine2 spine3 spine4 ... End

# Select the root of the chain
# Give a name
# Execute

tplt_1 = ["Root"]
tplt_2 = ["Root", "End"]
tplt_3 = ["Root", "Mid", "End"]
tplt_4 = ["Root", "Mid", "Tip", "End"]

templates = [tplt_1, tplt_2, tplt_3, tplt_4]
tplt_5 = ["Root", "End"]

# Parameters given by user
joint_name = "spine"
side = "m"

sel_list = mc.ls(selection = 1, long=1)
if len(sel_list) != 1:
    print("ERROR - Select the root joint.")
else:
    root_jnt = sel_list[0]
    print("Root joint: " + root_jnt)
    tmp_list = mc.listRelatives(ad=1, f=1)
    tmp_list.append(root_jnt)
    #NOTE: This list is reversed on purpose, 
    #      because we use full path, changing the parent will invalidate the child
    
    if len(tmp_list)>4:
        for i in range(len(tmp_list)-1, -1, -1):
            tmp_target_joint = tmp_list[-(i+1)]
            tmp_suffix = str(i+1)
            if i == len(tmp_list)-1:
                tmp_suffix = tplt_5[-1]
            elif i == 0:
                tmp_suffix = tplt_5[0]
            tmp_newName = side + "_" + joint_name + tmp_suffix + "_JNT"
            
            print(tmp_newName)
            print(tmp_target_joint)
            mc.select(tmp_target_joint)
            mc.rename(tmp_newName)
    else:
        tmp_tplt = templates[len(tmp_list)-1]
        for i in range(0, len(tmp_list)):
            tmp_target_joint = tmp_list[i]
            tmp_suffix = tmp_tplt[-(i+1)]
            tmp_newName = side + "_" + joint_name + tmp_suffix + "_JNT"
            print(tmp_newName)
            mc.select(tmp_target_joint)
            mc.rename(tmp_newName)
        
    
    
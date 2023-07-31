# This script aims to name bone chains automatically
# Root
# Root End
# Root Mid End
# Root Mid Tip End
# Root spine2 spine3 spine4 ... End

# 1.Select the root of the chain
# 2.Give a name and a side
# 3.Execute

import maya.cmds as cmds

# Create UI window  
window = cmds.window(title="RIG_001 - Batch Rename")  

# Column Layout
layout = cmds.columnLayout()
cmds.columnLayout( columnAttach=('both', 5), rowSpacing=10, columnWidth=250 )

# Title 
title = cmds.text(label='RIG_001 - Batch Rename')  

# Joint Name label  
label = cmds.text(label='Joint_Name')

# Text input field
text_name = cmds.textField()  

# Marker L
cb1 = cmds.checkBox(label='L')

# Marker M
cb2 = cmds.checkBox(label='M') 

# Marker R
cb3 = cmds.checkBox(label='R')

check_log = [False,False,False]

# Function to exclusive check 
def exclusiveCheck(wut):
    if cmds.checkBox(cb1, query=True, value=True) and not check_log[0]:
        cmds.checkBox(cb2, edit=True, value=False)
        cmds.checkBox(cb3, edit=True, value=False)
        check_log[1] = False
        check_log[2] = False
        check_log[0] = True
    elif cmds.checkBox(cb2, query=True, value=True) and not check_log[1]:
        cmds.checkBox(cb1, edit=True, value=False)
        cmds.checkBox(cb3, edit=True, value=False)
        check_log[0] = False
        check_log[2] = False
        check_log[1] = True
    elif cmds.checkBox(cb3, query=True, value=True) and not check_log[2]:
        cmds.checkBox(cb1, edit=True, value=False)
        cmds.checkBox(cb2, edit=True, value=False)
        check_log[1] = False
        check_log[0] = False
        check_log[2] = True

# Add callbacks to checkboxes          
cmds.checkBox(cb1, edit=True, changeCommand=exclusiveCheck)  
cmds.checkBox(cb2, edit=True, changeCommand=exclusiveCheck)
cmds.checkBox(cb3, edit=True, changeCommand=exclusiveCheck)


# Function to print selected prefixes + text input        
def printText(self):
    name_str = cmds.textField(text_name, query=True, text=True)    
    l = cmds.checkBox(cb1, query=True, value=True)  
    m = cmds.checkBox(cb2, query=True, value=True)
    r = cmds.checkBox(cb3, query=True, value=True)
    side_str = ((l * 'l') + (m * 'm') + (r * 'r'))
    
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
    joint_name = name_str
    side = side_str

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
            
# Button
button = cmds.button(label='Execute', command=printText)          

# Show UI window  
cmds.showWindow(window)
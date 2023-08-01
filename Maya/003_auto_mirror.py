import maya.cmds as mc

# This script will mirror all JNTs with l_ or r_ beginning
# This script will only operate on roots
            
def execute_mirror(*args):
    root_list = mc.ls("*Root_JNT")
    for j in root_list:
        mc.select(j)
        
        # Check if middle
        tmp_side = j.split("_")[0]
        
        if tmp_side == "l":
            # check if already mirror
            tmp_other = "r" + j[1:]
            tmp_checklist = mc.ls(tmp_other)
            if len(tmp_checklist)==0:
                mc.mirrorJoint(mirrorYZ=1, mirrorBehavior=1, searchReplace=("l_", "r_"))
        elif tmp_side == "r":
            tmp_other = "l" + j[1:]
            print(tmp_other)
            tmp_checklist = mc.ls(tmp_other)
            if len(tmp_checklist)==0:
                mc.mirrorJoint(mirrorYZ=1, mirrorBehavior=1, searchReplace=("r_", "l_"))

def create_rig003_window():
    if mc.window("RIG_003_window", exists=True):
        mc.deleteUI("RIG_003_window", window=True)
    
    window = mc.window("RIG_003_window", title="RIG_003 - Auto Mirror", widthHeight=(150, 100))
    mc.columnLayout(adjustableColumn=True)

    mc.text(label="RIG_003 - Auto Mirror", align="center", font="boldLabelFont", height=30)
    mc.button(label="Execute mirror", command=execute_mirror)

    mc.showWindow(window)

create_rig003_window()
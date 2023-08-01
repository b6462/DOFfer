import maya.cmds as mc

def single_group(*args):
    unite_name = mc.textField(text_field, query=True, text=True)
    sel_list = mc.ls(selection=1)
    for s in sel_list:
        tmp_name = s
        print(tmp_name)
        tmp_split = tmp_name.split("_")
        tmp_group_name = tmp_split[0] + "_" + tmp_split[1][:-4] + "_GRP"
        print(tmp_group_name)
        mc.select(s)
        mc.group()
        mc.rename(tmp_group_name)

def unite_group(*args):
    unite_name = mc.textField(text_field, query=True, text=True)
    sel_list = mc.ls(selection=1)
    tmp_name = sel_list[0]
    print(tmp_name)
    tmp_split = tmp_name.split("_")
    tmp_group_name = tmp_split[0] + "_" + unite_name + "_GRP"
    print(tmp_group_name)
    mc.group()
    mc.rename(tmp_group_name)


def create_rig004_window():
    if mc.window("RIG_004_window", exists=True):
        mc.deleteUI("RIG_004_window", window=True)
    
    window = mc.window("RIG_004_window", title="RIG_004 - Grouper", widthHeight=(250, 150))
    mc.columnLayout(adjustableColumn=True)
    mc.text(label="RIG_004 - Grouper", align="center", font="boldLabelFont", height=30)

    mc.text(label="Enter group name:", align="left")
    global text_field
    text_field = mc.textField(placeholderText="GroupName")

    mc.button(label="Unite all select to one group", command=unite_group)
    mc.button(label="Each select to one group", command=single_group)

    mc.showWindow(window)

create_rig004_window()
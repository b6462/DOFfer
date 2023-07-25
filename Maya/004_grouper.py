import maya.cmds as mc

# If true, will unite all selected nodes to one group
bUnite = False
unite_name = "hand"

sel_list = mc.ls(selection=1)

if bUnite:
    tmp_name = sel_list[0]
    print(tmp_name)
    tmp_split = tmp_name.split("_")
    tmp_group_name = tmp_split[0] + "_" + unite_name + "_GRP"
    print(tmp_group_name)
    mc.group()
    mc.rename(tmp_group_name)
else:
    for s in sel_list:
        tmp_name = s
        print(tmp_name)
        tmp_split = tmp_name.split("_")
        tmp_group_name = tmp_split[0] + "_" + tmp_split[1][:-4] + "_GRP"
        print(tmp_group_name)
        mc.select(s)
        mc.group()
        mc.rename(tmp_group_name)
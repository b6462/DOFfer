from maya.api.OpenMaya import MVector, MMatrix, MPoint
import maya.cmds as mc
import maya.mel as mel

# This script will wrap the selected curves with proper transform groups

sel_list = mc.ls(selection=1)
for sel in sel_list:
    base_name = sel
    markers = ["_pri", "_sec", "_drv", "_con", "_ofs"]
    
    mc.select(sel)
    for i in range(0, 5):
        tgt = mc.ls(selection=1)[0]
        name = base_name+markers[i]
        mc.group(tgt, a=1, n=name)
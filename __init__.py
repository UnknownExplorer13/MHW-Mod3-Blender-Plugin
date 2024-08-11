# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:38:47 2019

@author: AsteriskAmpersand
"""
# from .dbg import dbg_init
# dbg_init()

# Values sorted according to how they appear in Blender's UI
bl_info = {
    "name": "Monster Hunter World Model Importer/Exporter",
    "description": "Import & export MOD3 files from/for Monster Hunter World. (.mod3)",
    "location": "File > Import-Export > Monster Hunter World Mesh",
    "author": "AsteriskAmpersand (Code), CrazyT (Structure), UnknownExplorer13 (Current Plugin Fork)",
    "version": (2,1,0),
    "blender": (4,0,0),
    "tracker_url": "https://github.com/UnknownExplorer13/MHW-Mod3-Blender-Plugin/issues",
    "doc_url": "https://github.com/Ezekial711/MonsterHunterWorldModding/wiki/Asterisk's-Plugin-Features", # Written for the original 2.79 plugin but still relevant for my fork
    "category": "Import-Export"
}

import bpy

from .operators.mod3properties import symmetricPair
from .operators.mod3import import ImportMOD3
from .operators.mod3export import ExportMOD3
from .operators.mod3import import menu_func_import as mhw_model_menu_func_import
from .operators.mod3export import menu_func_export as mhw_model_menu_func_export

def register():
    bpy.utils.register_class(ImportMOD3)
    bpy.utils.register_class(ExportMOD3)
    bpy.types.TOPBAR_MT_file_import.append(mhw_model_menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(mhw_model_menu_func_export)
    bpy.types.Object.MHW_Symmetric_Pair = symmetricPair


def unregister():
    del bpy.types.Object.MHW_Symmetric_Pair
    bpy.utils.unregister_class(ImportMOD3)
    bpy.utils.unregister_class(ExportMOD3)
    bpy.types.TOPBAR_MT_file_import.remove(mhw_model_menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(mhw_model_menu_func_export)

    #del bpy.types.Object.MHWSkeleton

if __name__ == "__main__":
    register()

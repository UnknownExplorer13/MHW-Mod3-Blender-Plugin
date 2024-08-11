# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 00:14:32 2019

@author: AsteriskAmpersand
"""

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import EnumProperty, BoolProperty, StringProperty
from bpy.types import Operator

from ..mod3 import Mod3ExporterLayer as Mod3EL
from ..blender import BlenderMod3Exporter as Api
from ..blender.BlenderSupressor import SupressBlenderOps

class Context():
    def __init__(self, path, meshes, armature):
        self.path = path

class ExportMOD3(Operator, ExportHelper):
    bl_idname = "custom_export.export_mhw_mod3"
    bl_label = "Export MOD3"
    bl_options = {'REGISTER', 'PRESET', 'UNDO'}
    __doc__ = "Write a MOD3 file"

    # ImportHelper mixin class uses this
    filename_ext = ".mod3"
    filter_glob: StringProperty(default = "*.mod3", options = {'HIDDEN'}, maxlen = 255)

    split_normals: BoolProperty(
        name = "Use Custom Normals",
        description = "Use split/custom normals instead of Blender's auto-generated normals",
        default = True)
    highest_lod: BoolProperty(
        name = "Set Mesh Parts to Highest LOD",
        description = "Overwrites all mesh parts' explicit LODs to the highest LOD",
        default = True)
    coerce_fourth: BoolProperty(
        name = "Coerce 4th Negative Weight",
        description = "Forces non-explicit 4 weight vertices into a 4 weight blocktype",
        default = True)
    export_hidden: BoolProperty(
        name = "Export Hidden Meshes",
        description = "Exports hidden meshes along with visible meshes",
        default = True)
    export_bounds: EnumProperty(
        name = "Export Mesh Bounding Box",
        description = "Overrides the file bounding boxes",
        items= [("Calculate", "Calculate", "Recalculates a box for each mesh", 0),
                ("Explicit", "Explicit", "Exports Lattices as Bounding Boxes", 1)
                ],
        default = "Calculate",
        )
    errorItems = [("Ignore", "Ignore", "Will not log warnings. Catastrophical errors will still break the process", 0),
                  ("Warning", "Warning", "Will be logged as a warning. These are displayed in the console. (Window > Toggle System Console)", 1),
                  ("Error", "Error", "Will stop the exporting process. An error will be displayed and the log will show details. (Window > Toggle System Console)", 2),
                  ]
    levelProperties = ["propertyLevel", "blocktypeLevel", "loopLevel", "uvLevel", "colourLevel", "weightLevel", "weightCountLevel"]
    levelNames = ["Property Error Level", "Blocktype Error Level", "Loops Error Level", "UV Error Level", "Colour Error Level", "Weighting Error Level", "Weight Count Error Level"]
    levelDescription = ["Missing and Duplicated Header Properties",
                        "Conflicting Blocktype Declarations",
                        "Redundant, Mismatched and Missing Normals",
                        "UV Map Incompatibilities",
                        "Colour Map Incompatibilities",
                        "Vertex Weight Groups Irregularities",
                        "Weight Count Errors"]
    levelDefaults = ["Warning", "Error", "Ignore", "Error", "Ignore", "Warning", "Warning", "Error"]
    propString = """EnumProperty(
                    name = name,
                    description = desc,
                    items = errorItems,
                    default = pred)"""
    for prop, name, desc, pred in zip(levelProperties, levelNames, levelDescription, levelDefaults):
        exec("%s : %s"%(prop, propString))

    def execute(self, context):
        self.cleanScene(context)
        BApi = Api.BlenderExporterAPI()
        with SupressBlenderOps():
            try:
                bpy.ops.object.mode_set(mode = 'OBJECT')
            except:
                pass
            bpy.ops.object.select_all(action = 'DESELECT')
            for obj in bpy.context.scene.objects:
                obj.select_set(obj.type == "MESH")
            bpy.ops.object.transform_apply(location = True, rotation = True, scale = True)
            bpy.ops.object.select_all(action = 'DESELECT')

        options = self.parseOptions()
        Mod3EL.ModelToMod3(BApi, options).execute(self.properties.filepath)
        with SupressBlenderOps():
            bpy.ops.object.select_all(action = 'DESELECT')
            for ob in bpy.context.selected_objects:
                ob.select_set(False)
        # bpy.ops.object.mode_set(mode = 'OBJECT')
        # bpy.context.area.type = 'INFO'
        return {'FINISHED'}

    @staticmethod
    def cleanScene(context):
        data = set(bpy.data.objects)
        scene = set(bpy.context.scene.objects)
        for obj in data.difference(scene):
            bpy.data.objects.remove(obj)

    def parseOptions(self):
        options = {
                "lod": self.highest_lod,
                "levels": {prop: self.__getattribute__(prop) for prop in self.levelProperties},
                "splitnormals": self.split_normals,
                "coerce": self.coerce_fourth,
                "hidden": self.export_hidden,
                "boundingbox": self.export_bounds,
                }
        return options

def menu_func_export(self, context):
    self.layout.operator(ExportMOD3.bl_idname, text="Monster Hunter World Mesh (.mod3)")
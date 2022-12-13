bl_info = {
    "name": "Randomize LocRotScale",
    "author": "J. \"Dragonrider's Fury/DragonFury128\" D.",
    "version": (1, 0),
    "blender": (2, 79, 7),
    "location": "View3D > Object > Randomize Location/Rotation/Scale",
    "description": "Randomizes the locations (and optionally rotations and scales) of a named set of objects",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}


import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from math import radians
from random import random as rnd, uniform as unf
from bpy.props import *


#def rndLocRotScl(self, targetName, maxRot, maxScl, maxRange):
def rlrs(self, context):
    targetName = self.targetName
    maxRange = self.maxRange
    selectedOnly = self.selectedOnly
    doRot = self.doRot
    maxRot = self.maxRot
    doScale = self.doScale
    maxScale = self.maxScale
    minScale = self.minScale
    
    #Sanity checking
    if targetName == "": raise RuntimeError("Must set a Target Name.")
    if maxRot == 0: doRot = False
    if maxScale == 0: doScale = False
    if maxScale < minScale: raise ValueError("Min Scale cannot exceed Max Scale.")
    ###
    
    if selectedOnly:
        ol = bpy.context.selected_objects
    else:
        ol = bpy.data.objects
    
    print(ol)
    
    for o in ol:
        if o.name.startswith(targetName):
            o.location.x = rnd() * maxRange - maxRange / 2
            o.location.y = rnd() * maxRange - maxRange / 2
            o.location.z = rnd() * maxRange - maxRange / 2
            
            if doScale:
                o.scale.x = unf(minScale, maxScale)
                o.scale.y = unf(minScale, maxScale)
                o.scale.z = unf(minScale, maxScale)
            else:
                o.scale.x = 1
                o.scale.y = 1
                o.scale.z = 1
                
            if doRot:
                o.rotation_euler.x = radians(rnd() * maxRot)
                o.rotation_euler.y = radians(rnd() * maxRot)
                o.rotation_euler.z = radians(rnd() * maxRot)
            else:
                o.rotation_euler.x = 0
                o.rotation_euler.y = 0
                o.rotation_euler.z = 0


class OBJECT_OT_rlrs(Operator):
    bl_idname = "objects.rlrs"
    bl_label = "Randomize Location/Rotation/Scale"
    bl_options = {'REGISTER', 'UNDO'}
    
    targetName = StringProperty(
        name="Target Object",
        default="obj",
        description="The name prefix of the objects you wish to randomize",
    )
    
    maxRange = FloatProperty(
        name="Max Range",
        default=(50.0),
        min=0.0,
        soft_max=5000.0,
        description="The maximum offset that can be set for the source object",
    )
    
    selectedOnly = BoolProperty(
        name="Only Selected",
        default=True,
        description="Only randomize SELECTED objects that match the Target Object name",
    )
    
    doRot = BoolProperty(
        name="Randomize Rotation",
        default=False,
        description="Randomize source object rotation",
    )
    maxRot = FloatProperty(
        name="Max Rotation",
        soft_min=-360.0,
        soft_max=360.0,
        default=(360.0),
        description="The maximum rotation value that can be set for the source object",
    )
    
    doScale = BoolProperty(
        name="Randomize Scale",
        default=True,
        description="Randomize source object scale",
    )
    maxScale = FloatProperty(
        name="Max Scaling",
        min=0.0,
        soft_min=0.0,
        soft_max=100.0,
        default=(15.0),
        description="The maximum scale value that can be set for the source object",
    )
    minScale = FloatProperty(
        name="Min Scaling",
        min=0.0,
        soft_min=1,
        soft_max=100.0,
        default=(1.0),
        description="The minimum scale value that can be set for the source object",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'targetName')
        layout.prop(self, 'maxRange')
        layout.prop(self, 'selectedOnly')
        layout.separator()
        
        sclOpts = layout.row()
        sclOpts.prop(self, 'doScale')
        sclOpts.prop(self, 'minScale')
        sclOpts.prop(self, 'maxScale')
        
        rotOpts = layout.row()
        rotOpts.prop(self, 'doRot')
        rotOpts.prop(self, 'maxRot')

    #def execute(self, targetName, maxRot, maxScl, maxRange):
    def execute(self, context):

        #rndLocRotScl(self, targetName, maxRot, maxScl, maxRange)
        rlrs(self, context)

        return {'FINISHED'}


# Registration

def rlrs_button(self, context):
    self.layout.operator(
        OBJECT_OT_rlrs.bl_idname,
        text="Randomize Location/Rotation/Scale",
        icon='STICKY_UVS_DISABLE'
    )

"""
# This allows you to right click on a button and link to the manual
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/dev/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "editors/3dview/object"),
    )
    return url_manual_prefix, url_manual_mapping
"""

def register():
    bpy.utils.register_class(OBJECT_OT_rlrs)
    #bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_object.append(rlrs_button)
    """try:
        bpy.types.VIEW3D_MT_Object.prepend(OBJECT_OT_rlrs)
    except:
        pass"""


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_rlrs)
    #bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_object.remove(rlrs_button)
    
    """bpy.types.VIEW3D_MT_object.remove(VIEW3D_BoolTool_Menu)
    try:
        bpy.types.VIEW3D_MT_Object.remove(VIEW3D_BoolTool_Menu)
    except:
        pass"""


if __name__ == "__main__":
    register()

bl_info = {
    "name": "Curve: Randomize Point Radius",
    "author": "J. \"Dragonrider's Fury/DragonFury128\" D.",
    "version": (1, 0),
    "blender": (2, 79, 7),
    "location": "Edit Mode> Curve > Randomize CurvePoints Radii",
    "description": "Randomizes the radius of each selected CurvePoint to within a set range",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}


import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from random import random as rnd, uniform as unf
from bpy.props import *


#def rndLocRotScl(self, targetName, maxRot, maxScl, maxRange):
def randomize_points_radii(self, context):
    maxRad = self.maxRad
    minRad = self.minRad
    rel = self.rel
    clamp = self.clamp
    
    #Sanity checking
    if maxRad < minRad: raise ValueError("Min Radius cannot exceed Max Radius.")
    ###
    
    editObj = bpy.context.active_object
    
    if editObj.type != "CURVE": raise TypeError("Only valid on Curve objects!  I don't know how you called this function, but that should not be possible.")
    
    for s in editObj.data.splines:
        for p in s.points:
            if p.select:
                if rel:
                    p.radius = p.radius * unf(minRad, maxRad)
                    if p.radius > maxRad and clamp:
                        p.radius = maxRad
                else:
                    p.radius = unf(minRad, maxRad)

class OBJECT_OT_randomize_points_radii(Operator):
    bl_idname = "curve.randomize_points_radii"
    bl_label = "Randomize CurvePoints Radii"
    bl_description = "Randomize the radius of each selected CurvePoint to within a given range"
    bl_options = {'REGISTER', 'UNDO'}
    
    maxRad = FloatProperty(
        name="Max Radius",
        min=0.0,
        soft_max=10.0,
        default=(5.0),
        description="The maximum radius that can be set on any CurvePoint",
    )
    minRad = FloatProperty(
        name="Min Radius",
        min=0.0,
        soft_max=10.0,
        default=(0.0),
        description="The minimum radius that can be set on any CurvePoint",
    )
    rel = BoolProperty(
        name="Relative",
        default=False,
        description="Use relative randomization by multiplying each new CurvePoint radius by the pre-existing one.  (Note that without Clamp, this means that Max Radius is not actually the *MAX* radius.)"
    )
    clamp = BoolProperty(
        name="Clamp",
        default=True,
        description="Enforce Max Radius. (Only has an effect when using Relative randomization.)"
    )

    def draw(self, context):
        layout = self.layout
        
        r1 = layout.row()
        r1.prop(self, 'minRad')
        r1.prop(self, 'maxRad')
        
        r2 = layout.row()
        r2.prop(self, 'rel')
        r2.prop(self, 'clamp')

    #def execute(self, targetName, maxRot, maxScl, maxRange):
    def execute(self, context):

        #rndLocRotScl(self, targetName, maxRot, maxScl, maxRange)
        randomize_points_radii(self, context)

        return {'FINISHED'}


# Registration

def randomize_points_radii_button(self, context):
    self.layout.operator(
        OBJECT_OT_randomize_points_radii.bl_idname,
        text="Randomize CurvePoints Radii",
        icon='ALIGN'
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
    bpy.utils.register_class(OBJECT_OT_randomize_points_radii)
    #bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_edit_curve.append(randomize_points_radii_button)
    """try:
        bpy.types.VIEW3D_MT_Object.prepend(OBJECT_OT_rlrs)
    except:
        pass"""


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_randomize_points_radii)
    #bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_edit_curve.remove(randomize_points_radii_button)
    
    """bpy.types.VIEW3D_MT_object.remove(VIEW3D_BoolTool_Menu)
    try:
        bpy.types.VIEW3D_MT_Object.remove(VIEW3D_BoolTool_Menu)
    except:
        pass"""


if __name__ == "__main__":
    register()

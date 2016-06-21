# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "QuickScene Build",
    "description": "Quickly creates a small scene for testing textures, materials, etc.",
    "author": "Joseph L. Davis",
    "version": (1, 0, 0),
    "blender": (2, 74, 0),
    "location": "View3D > Add > Mesh > QuickScene Build",
    "warning": "No man page. For info, E-mail r8jewels@gofast.am, or click on the 'Documentation' button below.",
    "support": "TESTING", # OFFICIAL, COMMUNITY, TESTING.
    "wiki_url": "mailto:r8jewels@gofast.am",
    "category": "Add Mesh"
    }

import bpy
from bpy_extras import object_utils

Reg = 1

'''if "bpy" in locals():
    import imp
    imp.reload(QuickScene_Build)
else:
    from . import QuickScene_Build   
'''    

########!!!!!!!! **EXPERIMENTAL BEYOND THIS POINT!** !!!!!!!!######## 
#"""
def quickscene_build(self, context):
    
    bpy.ops.mesh.primitive_plane_add(radius=10)
    bpy.ops.mesh.primitive_cube_add(location=(4,0,1))
    bpy.ops.mesh.primitive_cone_add(location=(-4,0,1))
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0,4,1))
    bpy.ops.mesh.primitive_monkey_add(location=(0,-4,.75),rotation=(-20,0,45))
    bpy.ops.mesh.primitive_torus_add(location=(0,0,.25))

    print('Quick Scene added Successfully!')
    print(bpy.data.objects)
    
    #Begin applying transforms to our created objects...
    print('Beginning transforms application...')
    
    #First of all, deselect everything, so we're not working 
     #with all the wrong objects...
    bpy.ops.object.select_all(action='DESELECT')
    
    #Next, select all Mesh objects, because those are the ones we want
     #to be working with.
    bpy.ops.object.select_by_type(type='MESH')
    
    #Now, the last leg of this fuction: apply the transforms...
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    #...and deselect everything.
    bpy.ops.object.select_all(action='DESELECT')
    
   

class OBJECT_OT_quickscene_build(bpy.types.Operator):
    
    bl_idname = "mesh.quickscene_build"
    bl_label = "Quick Scene Build"
    bl_description = "Quickly Build a Scene"
    bl_options = {'REGISTER', 'UNDO'}    
    
    ##view_align = bpy.props.BoolProperty(
    ##        name="Align to View",
    ##        default=False
    ##        )
    ##
    ##location = bpy.props.FloatVectorProperty(
    ##        name="Location",
    ##        subtype='TRANSLATION',
    ##        )
    ##rotation = bpy.props.FloatVectorProperty(
    ##        name="Rotation",
    ##        subtype='EULER',
    ##        ) 
    
    
    def draw(self, context):
        layout = self.layout
        ##layout.prop(self, 'view_align')
        ##col = layout.column()
        ##col.prop(self, 'location')
        ##col.prop(self, 'rotation')
        
        
    def execute(self, context):

        quickscene_build(self, context)

        return {'FINISHED'}
#"""
#######!!!!!!!!!! **EXPERIMENTAL SECTION ENDING** !!!!!!!!!!########



# Define the "Quickscene_Build" menu
#class quickscenebuildMenu(bpy.types.Menu):
#    bl_idname = "quickscenebuildMenu"
#    bl_label = "QuickScene Build"
#
#    def draw(self, context):
#        layout = self.layout
#        layout.operator_context = 'INVOKE_REGION_WIN'
#        layout.operator("mesh.quickscene_build",text="QuickScene Build",icon="MOD_PATICLES")     
#

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_quickscene_build.bl_idname,
        text="QuickScene Build",
        icon='MOD_PARTICLES')

# Handle (menu) operators and panels
#def menu_func(self, context):
#    self.layout.menu("quickscenebuildMenu",icon="MOD_PARTICLES")

def register():
    bpy.utils.register_class(OBJECT_OT_quickscene_build)
    #bpy.utils.register_module(__name__)
    #bpy.types.INFO_MT_mesh_add.append(menu_func)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_quickscene_build)
    #bpy.utils.unregister_module(__name__)
    #bpy.types.INFO_MT_mesh_add.remove(menu_func)
    bpy.types.INFO_MT_mesh_add.remove(add_object_button)

if __name__ == "__main__" and Reg == 1:
    register()
#elif __name__ != "__main__" or Reg != 1:
#    unregister()
#else:
#    unregister()
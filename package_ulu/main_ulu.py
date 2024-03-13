'''
Copyright (C) 2024 Arik Salehi
https://ariksalehi.com

frostwizard4@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import math
import bpy                                                                                              #type:ignore              
from bpy.types import Operator                                                                          #type:ignore
from bpy.props import FloatProperty, EnumProperty, BoolProperty                                         #type:ignore

class OBJECT_OT_unwraplayoutuv(Operator):
    """UV Smart Project and set Texel Density + Texture Size"""                                         # Use this as a tooltip for menu items and buttons
    bl_idname = "object.unwraplayoutuv"                                                                 # Unique identifier for buttons and menu items to reference
    bl_label = "Unwrap and Layout UV's"                                                                 # Display name in the interface
    bl_options = {'REGISTER', 'UNDO'}                                                                   # Enable undo for the operator

    enum_items = [
        ("SCALED", "Scaled", "Use scale of existing UVs to multiply margin"),
        ("ADD", "Add", "Just add the margin, ignoring any UV scale")
    ]
    texDensityProp: FloatProperty(name = "Texel Density", min=0.01, default=1.0)                        #type:ignore Define Properties for plugin controls
    sp_AngleProp: FloatProperty(name = "Angle Limit", min=0.0, max=90.0, default=45.0)                  #type:ignore
    sp_MarginMethod: EnumProperty(name = "Margin Method", items=enum_items, default="SCALED")           #type:ignore
    sp_IslandMargin: FloatProperty(name = "Island Margin", min=0.0, max=1.0, default=0.0, precision=3)  #type:ignore
    sp_AreaWeight: FloatProperty(name = "Area Weight", min=0.0, max=1.0, default=0.0, precision=3)      #type:ignore
    sp_CorrectAspect: BoolProperty(name = "Correct Aspect", default=True)                               #type:ignore
    sp_ScaleBounds: BoolProperty(name = "Scale to Bounds", default=False)                               #type:ignore

    def execute(self, context):                                                                         # execute() is called when running the operator
        override_window = context.window
        override_screen = override_window.screen
        override_area = [area for area in override_screen.areas if area.type == "VIEW_3D"]
        override_region = [region for region in override_area[0].regions if region.type == 'WINDOW']

        with context.temp_override(window=override_window, area=override_area[0], region=override_region[0]):
            collection = bpy.context.collection                                                             # Get currently selected collection
            selection_names = []                                                                            # Declare array to hold objects to iterate on

            self.report({'INFO'}, f"texDensityProp: {self.texDensityProp}")
            self.report({'INFO'}, f"sp_AngleProp: {self.sp_AngleProp}")
            self.report({'INFO'}, f"sp_MarginMethod: {self.sp_MarginMethod}")
            self.report({'INFO'}, f"sp_IslandMargin: {self.sp_IslandMargin}")
            self.report({'INFO'}, f"sp_AreaWeight: {self.sp_AreaWeight}")

            for obj in collection.objects:                                                                  # Get every object inside the collection selected
                if obj.type == 'MESH':                                                                      # Select only meshes
                    selection_names.append(obj)                                                             # Add to the array
                    obj.select_set(False)                                                                   # Deselect all objects

            if selection_names != []:                                                                       # Make sure there are items in the array
                for obj in selection_names:                                                                 # Get all objects in currently selected collection
                    bpy.context.view_layer.objects.active = obj                                             # Set it as actively selected
                    obj.select_set(True)                                                                    # Select the current object
                
                    uvMap = obj.data.uv_layers.new(name="ULU_UVMap")                                        # new UV layer for mapping
                    uvMap.active = True                                                                     # Set new map to active
                
                    bpy.ops.object.mode_set(mode = 'EDIT')                                                  # Change to edit mode
                    bpy.ops.mesh.select_all(action='SELECT')                                                # Select all vertices
                    try:                                                                                    # Encapsulate Texel Density Checker functions
                        bpy.context.scene.td.texture_size = '1'                                             # Set texture size to 1024
                    except AttributeError:                                                                  # If AttributeError thrown, run following line
                        self.report({'ERROR'}, "Texel Density Checker not installed!")                      # Show error message    
                    
                    bpy.ops.uv.smart_project(                                                               # Set up Smart UV Project
                        angle_limit=math.radians(self.sp_AngleProp),                                                    
                        margin_method=self.sp_MarginMethod, 
                        island_margin=self.sp_IslandMargin, 
                        area_weight=self.sp_AreaWeight, 
                        correct_aspect=self.sp_CorrectAspect, 
                        scale_to_bounds=self.sp_ScaleBounds
                    )
                    try:                                                                                    # Try running the following
                        bpy.ops.object.texel_density_check()                                                # Update Texel Density
                        texelDensity = bpy.context.scene.td.density                                         # Calculate Texel Density
                        if(texelDensity != 0):
                            updateDensity = round(((1024 * self.texDensityProp) / float(texelDensity)))     # Calculate perfect texel size
                        else:
                            updateDensity = 0
                        bpy.context.scene.td.texture_size = '4'                                             # Set texture size to "Custom"
                        bpy.context.scene.td.custom_width = str(updateDensity)                              # Set width to perfect size
                        bpy.context.scene.td.custom_height = str(updateDensity)                             # Set height to perfect size
                    except AttributeError:                                                                  # If AttributeError thrown, run following line
                        self.report({'ERROR'}, "Texel Density Checker not installed!")                      # Show error message

                    bpy.ops.object.mode_set(mode = 'OBJECT')                                                # Switch back to object mode     
                    obj.select_set(False)
        return {'FINISHED'}                                                                             # Lets Blender know the operator finished successfully.if
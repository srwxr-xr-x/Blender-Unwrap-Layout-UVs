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

bl_info = {
    "name": "UV Unwrap and Layout",
    "description": "Automatically Smart UV Project and change Texel Density + Texture Size.",
    "author": "Arik Salehi",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "doc_url": "",
    "location": "View3D > Object",
    "warning": "Requires the Texel Density Checker Addon!",
    "support": "COMMUNITY",
    "category": "UV",
}
import bpy

if ("main_ulu" not in locals()):
    from . import main_ulu
else:
    import importlib
    main_ulu = importlib.reload(main_ulu)

from . main_ulu import OBJECT_OT_unwraplayoutuv

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_unwraplayoutuv.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_unwraplayoutuv)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    print(f"Registered {bl_info['name']}")

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_unwraplayoutuv)

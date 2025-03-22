import bpy

class ANIM_PT_facing_settings(bpy.types.Panel):
    bl_idname = "ANIM_PT_facing_settings"
    bl_label = "Facing Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AnimFacer CnC Addon"
    bl_order = 1  # This ensures it appears first

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "num_faces", text="Number of Facings:")
        layout.prop(context.scene, "rotation_direction", text="Rotation Direction:")

def register():
    bpy.utils.register_class(ANIM_PT_facing_settings)

    # Define the properties
    bpy.types.Scene.num_faces = bpy.props.IntProperty(name="Number of Faces", default=8, min=1, max=32)
    bpy.types.Scene.rotation_direction = bpy.props.EnumProperty(
        name="Rotation Direction",
        items=[("CW", "Clockwise (vehicles)", ""), ("CCW", "CounterClockwise (infantry)", "")]
    )
    bpy.types.Scene.show_facing_settings = bpy.props.BoolProperty(
        name="Show Facing Settings",
        default=True
    )

def unregister():
    bpy.utils.unregister_class(ANIM_PT_facing_settings) 
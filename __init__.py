bl_info = {
    "name": "AnimFacer CnC Addon",
    "author": "Holland",
    "version": (1, 0, 0),  # Correct version format
    "blender": (4, 2, 0),  # Match the Blender version format
    "location": "View3D > N-Panel > AnimFacer CnC Addon",
    "description": "Addon for creating animations in multiple directions",
    "warning": "",
    "doc_url": "",
    "category": "Animation",
}

import bpy
from .ini_writer import ParentRigOperator
from .rotate_keyframe import RotateKeyframeOperator
from .action_cutter import PoseKeys2ActionProperties, CreateNewActionOperator, RemoveInBetweenKeysOperator, register_misc_tools_property
from .animation_manager import register as register_animation_manager, unregister as unregister_animation_manager
from .settings import register as register_settings, unregister as unregister_settings
from .scale_animations import register as register_scale_animations, unregister as unregister_scale_animations

class ANIM_PT_my_panel(bpy.types.Panel):
    bl_idname = "ANIM_PT_my_panel"
    bl_label = "Rotate any selected object"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AnimFacer CnC Addon"
    bl_order = 4  # This ensures it appears last
    bl_options = {'DEFAULT_CLOSED'}  # This makes the panel closed by default

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Rotate selected object")
        box.prop(context.scene, "rotation_faces", text="Rotation Facings")
        box.prop(context.scene, "skip_frames", text="Skip Frames")
        box.operator("object.rotate_keyframe_operator")

class ANIM_PT_misc_tools(bpy.types.Panel):
    bl_idname = "ANIM_PT_misc_tools"
    bl_label = "Misc Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AnimFacer CnC Addon"
    bl_order = 5  # This ensures it appears after the rotate panel
    bl_options = {'DEFAULT_CLOSED'}  # This makes the panel closed by default

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Create new action from selected keys (in Pose Mode):")
        props = context.scene.pose_keys_to_action_props
        box.prop(props, "action_name", text="Action Name")
        box.operator("pose.create_new_action", text="Create New Action")

        # Separator for visual separation
        box.separator()
        box.operator("pose.remove_in_between_keys", text="Remove In-between Keys")
        box.label(text="Removing excess data from external 3D tools can boost performance.")

def register():
    # Register in the correct order
    register_settings()  # First
    register_scale_animations()  # Second
    register_animation_manager()  # Third
    bpy.utils.register_class(ParentRigOperator)
    bpy.utils.register_class(RotateKeyframeOperator)
    bpy.utils.register_class(ANIM_PT_my_panel)
    bpy.utils.register_class(ANIM_PT_misc_tools)
    bpy.utils.register_class(PoseKeys2ActionProperties)
    bpy.utils.register_class(CreateNewActionOperator)
    bpy.utils.register_class(RemoveInBetweenKeysOperator)
    register_misc_tools_property()
    bpy.types.Scene.pose_keys_to_action_props = bpy.props.PointerProperty(
        type=PoseKeys2ActionProperties
    )

    # Define the properties
    bpy.types.Scene.rotation_faces = bpy.props.IntProperty(name="Rotation Facings", default=8, min=1, max=32)
    bpy.types.Scene.skip_frames = bpy.props.IntProperty(name="Skip Frames", default=1, min=1)

def unregister():
    # Unregister in reverse order
    bpy.utils.unregister_class(RemoveInBetweenKeysOperator)
    bpy.utils.unregister_class(CreateNewActionOperator)
    bpy.utils.unregister_class(PoseKeys2ActionProperties)
    bpy.utils.unregister_class(ANIM_PT_misc_tools)
    bpy.utils.unregister_class(ANIM_PT_my_panel)
    bpy.utils.unregister_class(RotateKeyframeOperator)
    bpy.utils.unregister_class(ParentRigOperator)
    unregister_animation_manager()
    unregister_scale_animations()
    unregister_settings()

    # Delete the properties
    del bpy.types.Scene.pose_keys_to_action_props
    del bpy.types.Scene.show_misc_tools
    del bpy.types.Scene.rotation_faces
    del bpy.types.Scene.skip_frames

if __name__ == "__main__":
    register()
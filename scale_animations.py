import bpy

class ScaleAnimationOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.scale_animation"
    bl_label = "Scale Animation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the selected animation and the desired number of frames
        anim = getattr(context.scene, "scale_animation")
        num_frames = context.scene.scale_num_frames

        # Get the action
        action = bpy.data.actions.get(anim)
        if action:
            # Calculate the scaling factor
            scale_factor = num_frames / (action.frame_range[1] - action.frame_range[0])
            
            # Scale the action's F-Curves
            for fcurve in action.fcurves:
                for keyframe_point in fcurve.keyframe_points:
                    keyframe_point.co.x *= scale_factor
                    keyframe_point.handle_left.x *= scale_factor
                    keyframe_point.handle_right.x *= scale_factor

            self.report({'INFO'}, f"Animation scaled to {num_frames} frames")
        return {'FINISHED'}

class ANIM_PT_scale_animations(bpy.types.Panel):
    bl_idname = "ANIM_PT_scale_animations"
    bl_label = "Scale Animations"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AnimFacer CnC Addon"
    bl_order = 2  # This ensures it appears after the facing settings panel
    bl_options = {'DEFAULT_CLOSED'}  # This makes the panel closed by default

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Scale animations if needed:")
        row = box.row()
        row.prop_search(context.scene, "scale_animation", bpy.data, "actions", text="")
        row.prop(context.scene, "scale_num_frames", text="")
        row.operator("object.scale_animation", text="Scale")

def register():
    bpy.utils.register_class(ScaleAnimationOperator)
    bpy.utils.register_class(ANIM_PT_scale_animations)

    # Define the properties
    bpy.types.Scene.scale_animation = bpy.props.StringProperty(name="Scale Animation")
    bpy.types.Scene.scale_num_frames = bpy.props.IntProperty(name="Scale Num Frames", default=1, min=1)

def unregister():
    bpy.utils.unregister_class(ScaleAnimationOperator)
    bpy.utils.unregister_class(ANIM_PT_scale_animations) 
import bpy

class ScaleAnimationOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.scale_animation_operator"
    bl_label = "Scale"

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

        return {'FINISHED'}

def register():
    bpy.utils.register_class(ScaleAnimationOperator)

def unregister():
    bpy.utils.unregister_class(ScaleAnimationOperator)
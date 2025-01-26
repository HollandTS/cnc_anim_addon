import bpy
import math

class RotateKeyframeOperator(bpy.types.Operator):
    """Rotate selected object"""
    bl_idname = "object.rotate_keyframe_operator"
    bl_label = "Rotate"

    def execute(self, context):
        obj = context.object  # Get the selected object
        num_faces = context.scene.rotation_faces
        rotation_direction = context.scene.rotation_direction
        skip_frames = context.scene.skip_frames  # Get the skip frames value

        angle_increment = 360 / num_faces

        for i in range(num_faces):
            angle = i * angle_increment
            obj.rotation_euler.z = -math.radians(angle) if rotation_direction == "CW" else math.radians(angle)
            obj.keyframe_insert(data_path="rotation_euler", frame=(i * skip_frames) + 1)  # Apply skip frames

        # Set the interpolation type to constant for each keyframe
        fcurves = obj.animation_data.action.fcurves
        for fcurve in fcurves:
            if fcurve.data_path == "rotation_euler":
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'CONSTANT'

        return {'FINISHED'}
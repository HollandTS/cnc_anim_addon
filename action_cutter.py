import bpy

class PoseKeys2ActionProperties(bpy.types.PropertyGroup):
    action_name: bpy.props.StringProperty(
        name="Action Name",
        description="Enter a name for the new action",
        default="NewAction",
    )

class CreateNewActionOperator(bpy.types.Operator):
    """Operator to create a new action from selected keyframes."""
    bl_idname = "pose.create_new_action"
    bl_label = "Create New Action"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        props = context.scene.pose_keys_to_action_props

        # Validation: Ensure in Pose Mode and armature selected
        if not obj or obj.type != 'ARMATURE' or context.mode != 'POSE':
            self.report({'ERROR'}, "Please select an armature and switch to Pose Mode.")
            return {'CANCELLED'}

        anim_data = obj.animation_data
        if not anim_data or not anim_data.action:
            self.report({'ERROR'}, "No action found on the selected object.")
            return {'CANCELLED'}

        current_action = anim_data.action

        # Create a new action
        new_action_name = props.action_name.strip()
        if not new_action_name:
            self.report({'ERROR'}, "Action name cannot be empty.")
            return {'CANCELLED'}

        new_action = bpy.data.actions.new(name=new_action_name)
        new_action.use_fake_user = True  # Enable Fake User for the new action
        obj.animation_data.action = new_action

        # Copy selected keyframes
        selected_keyframes = self.get_selected_keyframes(current_action)
        if not selected_keyframes:
            self.report({'ERROR'}, "No keyframes selected.")
            return {'CANCELLED'}

        for fcurve in current_action.fcurves:
            # Create equivalent FCurve in new action
            new_fcurve = new_action.fcurves.new(data_path=fcurve.data_path, index=fcurve.array_index)
            for frame in selected_keyframes:
                for keyframe_point in fcurve.keyframe_points:
                    if frame == keyframe_point.co[0]:
                        new_fcurve.keyframe_points.insert(frame, keyframe_point.co[1])
                        break

        self.report({'INFO'}, f"New action '{new_action_name}' created.")
        return {'FINISHED'}

    @staticmethod
    def get_selected_keyframes(action):
        """Retrieve selected keyframes from the active action."""
        selected_frames = set()
        for fcurve in action.fcurves:
            for keyframe_point in fcurve.keyframe_points:
                if keyframe_point.select_control_point:
                    selected_frames.add(keyframe_point.co[0])  # Add frame to set
        return sorted(selected_frames)

class RemoveInBetweenKeysOperator(bpy.types.Operator):
    """Operator to remove in-between keys."""
    bl_idname = "pose.remove_in_between_keys"
    bl_label = "Remove In-between Keys"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        remove_in_between_keys()
        self.report({'INFO'}, "In-between keyframes removed successfully!")
        return {'FINISHED'}

def remove_in_between_keys():
    # Check for pose mode and selected bones
    if bpy.context.mode == 'POSE' and bpy.context.object.type == 'ARMATURE':
        for bone in bpy.context.selected_pose_bones:
            action = bpy.context.object.animation_data.action
            if action:
                for fcurve in action.fcurves:
                    if fcurve.data_path.startswith(f'pose.bones["{bone.name}"]'):
                        # Collect keyframes to remove
                        keyframes_to_remove = [
                            i for i, keyframe_point in enumerate(fcurve.keyframe_points)
                            if not keyframe_point.co[0].is_integer()
                        ]
                        # Remove keyframes in reverse order (to avoid index shifting)
                        for index in sorted(keyframes_to_remove, reverse=True):
                            try:
                                fcurve.keyframe_points.remove(fcurve.keyframe_points[index])
                            except RuntimeError as e:
                                print(f"Could not remove keyframe at index {index}: {e}")
    
    # Check for object mode and selected objects
    elif bpy.context.mode == 'OBJECT':
        for obj in bpy.context.selected_objects:
            if obj.animation_data and obj.animation_data.action:
                action = obj.animation_data.action
                for fcurve in action.fcurves:
                    # Collect keyframes to remove
                    keyframes_to_remove = [
                        i for i, keyframe_point in enumerate(fcurve.keyframe_points)
                        if not keyframe_point.co[0].is_integer()
                    ]
                    # Remove keyframes in reverse order
                    for index in sorted(keyframes_to_remove, reverse=True):
                        try:
                            fcurve.keyframe_points.remove(fcurve.keyframe_points[index])
                        except RuntimeError as e:
                            print(f"Could not remove keyframe at index {index}: {e}")

# Property to show/hide Misc Tools
def register_misc_tools_property():
    bpy.types.Scene.show_misc_tools = bpy.props.BoolProperty(
        name="Show Misc Tools",
        description="Show or hide the Misc Tools section",
        default=False,
    )

# Registration
def register():
    bpy.utils.register_class(PoseKeys2ActionProperties)
    bpy.utils.register_class(CreateNewActionOperator)
    bpy.utils.register_class(RemoveInBetweenKeysOperator)
    register_misc_tools_property()
    bpy.types.Scene.pose_keys_to_action_props = bpy.props.PointerProperty(
        type=PoseKeys2ActionProperties
    )

def unregister():
    bpy.utils.unregister_class(PoseKeys2ActionProperties)
    bpy.utils.unregister_class(CreateNewActionOperator)
    bpy.utils.unregister_class(RemoveInBetweenKeysOperator)
    del bpy.types.Scene.pose_keys_to_action_props
    del bpy.types.Scene.show_misc_tools

if __name__ == "__main__":
    register()
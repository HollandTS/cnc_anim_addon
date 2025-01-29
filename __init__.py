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
from .animation_scaler import ScaleAnimationOperator
from .action_cutter import PoseKeys2ActionProperties, CreateNewActionOperator, RemoveInBetweenKeysOperator, register_misc_tools_property

class AddAnimationOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.add_animation_operator"
    bl_label = "Add Animation"

    def execute(self, context):
        context.scene.num_animations += 1
        
        # Set start and end frames of the playback/rendering range
        context.scene.frame_start = 0
        context.scene.frame_end = 0  # This will be dynamically updated during execution

        return {'FINISHED'}

class UndoExecutionOperator(bpy.types.Operator):
    """Operator to undo the execution and remove created strips and parent object."""
    bl_idname = "object.undo_execution"
    bl_label = "Remove"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object

        # Set the playhead to frame 0
        context.scene.frame_current = 0

        if obj and obj.type == 'ARMATURE':
            anim_data = obj.animation_data
            if anim_data:
                # Remove all NLA strips
                for track in anim_data.nla_tracks:
                    anim_data.nla_tracks.remove(track)
                
                # Remove the parent object
                if obj.parent and obj.parent.name.startswith("CircleArrow"):
                    bpy.data.objects.remove(obj.parent, do_unlink=True)

                # Clear the parent relationship
                obj.parent = None

        self.report({'INFO'}, "Execution undone successfully!")
        return {'FINISHED'}

class ANIM_PT_my_panel(bpy.types.Panel):
    bl_idname = "ANIM_PT_my_panel"
    bl_label = "AnimFacer CnC Addon"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AnimFacer CnC Addon"

    def draw(self, context):
        layout = self.layout

        # Section for scaling animations
        box = layout.box()
        box.label(text="Scale animations if needed:")
        row = box.row()
        row.prop_search(context.scene, "scale_animation", bpy.data, "actions", text="")
        row.prop(context.scene, "scale_num_frames", text="")
        row.operator("object.scale_animation_operator", text="Scale")  # Add the Scale button next to the slider

        # Section for adding animations
        box = layout.box()
        box.operator("object.add_animation_operator")

        # Section for selecting animations
        box = layout.box()
        box.label(text="Select Animations:")
        for i in range(1, context.scene.num_animations + 1):  # Use num_animations to determine how many to display
            row = box.row()
            row.prop_search(context.scene, f"animation_{i}", bpy.data, "actions", text="")
            if context.scene.rotation_direction == "CW":
                row.prop(context.scene, f"ini_entry_cw_{i}", text="")
            else:
                row.prop(context.scene, f"ini_entry_ccw_{i}", text="")
            row.prop(context.scene, f"compass_direction_{i}", text="")
            row.prop(context.scene, f"loop_clip_{i}", text="Loop Clip")

        # Section for specifying the number of faces
        box = layout.box()
        box.label(text="Number of Facings:")
        box.prop(context.scene, "num_faces", text="")

        # Section for choosing the rotation direction
        box = layout.box()
        box.label(text="Rotation Direction:")
        box.prop(context.scene, "rotation_direction", text="")

        # Larger button for the parent rig operator
        box = layout.box()
        row = box.row()
        row.scale_y = 1.5  # Make the button taller
        row.operator("object.parent_rig_operator")

        # Undo Execution section
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Undo execution:")
        row.operator("object.undo_execution", text="Remove", icon='CANCEL')

        # Section for keyframe rotation
        box = layout.box()
        box.label(text="Rotate selected object")
        box.prop(context.scene, "rotation_faces", text="Rotation Facings")
        box.prop(context.scene, "skip_frames", text="Skip Frames")  # Add Skip Frames slider
        box.operator("object.rotate_keyframe_operator")

        # Misc Tools Section
        box = layout.box()
        box.label(text="Misc Tools")
        box.prop(context.scene, "show_misc_tools", icon="TRIA_DOWN" if context.scene.show_misc_tools else "TRIA_RIGHT", emboss=False)
        if context.scene.show_misc_tools:
            box.label(text="Create new action from selected keys (in Pose Mode):")
            props = context.scene.pose_keys_to_action_props
            box.prop(props, "action_name", text="Action Name")
            box.operator("pose.create_new_action", text="Create New Action")

            # Separator for visual separation
            box.separator()
            box.operator("pose.remove_in_between_keys", text="Remove In-between Keys")
            box.label(text="Removing excess data from external 3D tools can boost performance.")

def register():
    bpy.utils.register_class(ParentRigOperator)
    bpy.utils.register_class(AddAnimationOperator)
    bpy.utils.register_class(RotateKeyframeOperator)
    bpy.utils.register_class(ScaleAnimationOperator)
    bpy.utils.register_class(UndoExecutionOperator)
    bpy.utils.register_class(ANIM_PT_my_panel)
    bpy.utils.register_class(PoseKeys2ActionProperties)
    bpy.utils.register_class(CreateNewActionOperator)
    bpy.utils.register_class(RemoveInBetweenKeysOperator)
    register_misc_tools_property()
    bpy.types.Scene.pose_keys_to_action_props = bpy.props.PointerProperty(
        type=PoseKeys2ActionProperties
    )

    # Define the properties
    bpy.types.Scene.num_faces = bpy.props.IntProperty(name="Number of Faces", default=8, min=1, max=32)
    bpy.types.Scene.num_animations = bpy.props.IntProperty(name="Number of Animations", default=10, min=1)  # New property
    bpy.types.Scene.rotation_direction = bpy.props.EnumProperty(
        name="Rotation Direction",
        items=[("CW", "Clockwise (vehicles)", ""), ("CCW", "CounterClockwise (infantry)", "")]
    )
    bpy.types.Scene.scale_animation = bpy.props.StringProperty(name="Scale Animation")  # New property
    bpy.types.Scene.scale_num_frames = bpy.props.IntProperty(name="Scale Num Frames", default=1, min=1)  # New property
    bpy.types.Scene.rotation_faces = bpy.props.IntProperty(name="Rotation Facings", default=8, min=1, max=32)  # New property for keyframe rotation
    bpy.types.Scene.skip_frames = bpy.props.IntProperty(name="Skip Frames", default=1, min=1)  # New skip frames property
    for i in range(1, 21):  # Create 20 animation selection properties
        setattr(bpy.types.Scene, f"animation_{i}", bpy.props.StringProperty(name=f"Animation {i}"))
        setattr(bpy.types.Scene, f"frame_count_{i}", bpy.props.IntProperty(name=f"Frame Count {i}"))  # Add a new property for the frame count
        setattr(bpy.types.Scene, f"ini_entry_cw_{i}", bpy.props.EnumProperty(
            items=[
                ("StandingFrames", "StandingFrames", ""),
                ("WalkFrames", "WalkFrames", ""),
                ("DeathFrames", "DeathFrames", ""),
                ("FiringFrames", "FiringFrames", ""),
                ("IdleFrames", "IdleFrames", "")
            ],
            name=f"INI Entries (Vehicles) {i}",
            default="StandingFrames" if i == 1 else "WalkFrames" if i == 2 else "DeathFrames" if i == 3 else "FiringFrames" if i == 4 else "IdleFrames"  # Set the default value
        ))
        setattr(bpy.types.Scene, f"ini_entry_ccw_{i}", bpy.props.EnumProperty(
            items=[
                ("Ready", "Ready", ""),
                ("Guard", "Guard", ""),
                ("Walk", "Walk", ""),
                ("Idle1", "Idle1", ""),
                ("Idle2", "Idle2", ""),
                ("Prone", "Prone", ""),
                ("Crawl", "Crawl", ""),
                ("FireUp", "FireUp", ""),
                ("FireProne", "FireProne", ""),
                ("Die1", "Die1", ""),
                ("Die2", "Die2", ""),
                ("FireProne", "FireProne", ""),
                ("Deploy", "Deploy", ""),
                ("Deployed", "Deployed", ""),
                ("DeployedFire", "DeployedFire", ""),
                ("DeployedIdle", "DeployedIdle", ""),
                ("Undeploy", "Undeploy", ""),
                ("Hover", "Hover", ""),
                ("Tumble", "Tumble", ""),
                ("FireFly", "FireFly", ""),
                ("Tread", "Tread", ""),
                ("Swim", "Swim", ""),
                ("WetAttack", "WetAttack", ""),
                ("WetIdle1", "WetIdle1", ""),
                ("WetIdle2", "WetIdle2", ""),
                ("WetDie1", "WetDie1", ""),
                ("WetDie2", "WetDie2", "")
            ],
            name=f"INI Entries (Infantry) {i}",
            default="Ready" if i == 1 else "Guard" if i == 2 else "Walk" if i == 3 else "Idle1" if i == 4 else "Idle2" if i == 5 else "Prone" if i == 6 else "Crawl" if i == 7 else "FireUp" if i == 8 else "FireProne" if i == 9 else "Die1"  # Set the default value
        ))
        setattr(bpy.types.Scene, f"compass_direction_{i}", bpy.props.EnumProperty(
            items=[
                ("All", "All", ""),
                ("N", "North", ""),
                ("NE", "Northeast", ""),
                ("E", "East", ""),
                ("SE", "Southeast", ""),
                ("S", "South", ""),
                ("SW", "Southwest", ""),
                ("W", "West", ""),
                ("NW", "Northwest", "")
            ],
            name=f"Compass Direction {i}",
            default="All"  # Set the default value
        ))
        setattr(bpy.types.Scene, f"loop_clip_{i}", bpy.props.BoolProperty(name=f"Loop Clip {i}", default=False))  # Add loop clip property

def update_rotation_direction(context):
    scene = context.scene
    if scene.rotation_direction == "CW":
        scene.loop_clip_1 = True  # Enable the first checkbox for vehicles
    elif scene.rotation_direction == "CCW":
        scene.loop_clip_1 = True  # Enable the first two checkboxes for infantry

def unregister():
    bpy.utils.unregister_class(ParentRigOperator)
    bpy.utils.unregister_class(AddAnimationOperator)
    bpy.utils.unregister_class(RotateKeyframeOperator)
    bpy.utils.unregister_class(ScaleAnimationOperator)
    bpy.utils.unregister_class(UndoExecutionOperator)
    bpy.utils.unregister_class(ANIM_PT_my_panel)
    bpy.utils.unregister_class(PoseKeys2ActionProperties)
    bpy.utils.unregister_class(CreateNewActionOperator)
    bpy.utils.unregister_class(RemoveInBetweenKeysOperator)
    del bpy.types.Scene.pose_keys_to_action_props
    del bpy.types.Scene.show_misc_tools

    # Delete the properties
    del bpy.types.Scene.num_faces
    del bpy.types.Scene.num_animations  # Delete the new property
    del bpy.types.Scene.rotation_direction
    del bpy.types.Scene.scale_animation  # Delete the new property
    del bpy.types.Scene.scale_num_frames  # Delete the new property
    del bpy.types.Scene.rotation_faces  # Delete the keyframe rotation property
    del bpy.types.Scene.skip_frames  # Delete the skip frames property
    for i in range(1, 21):  # Delete 20 animation selection properties
        delattr(bpy.types.Scene, f"animation_{i}")
        delattr(bpy.types.Scene, f"frame_count_{i}")  # Delete the frame count property
        delattr(bpy.types.Scene, f"ini_entry_cw_{i}")
        delattr(bpy.types.Scene, f"ini_entry_ccw_{i}")
        delattr(bpy.types.Scene, f"compass_direction_{i}")
        delattr(bpy.types.Scene, f"loop_clip_{i}")  # Delete the loop clip property

if __name__ == "__main__":
    register()
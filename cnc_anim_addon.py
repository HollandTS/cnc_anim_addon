bl_info = {
    "name": "C&C Anim Addon",
    "author": "Holland",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "View3D > N-Panel > C&C Anim Addon",
    "description": "Addon for creating animations in multiple directions",
    "warning": "",
    "doc_url": "",
    "category": "Animation",
}

import bpy
import math
import animation_scaler  # Import the animation_scaler module

# Global variable to keep track of whether animation_scaler has been registered
animation_scaler_registered = False

def get_compass_angle(direction):
    compass_directions = {
        "N": 0,
        "NE": 45,
        "E": 90,
        "SE": 135,
        "S": 180,
        "SW": 225,
        "W": 270,
        "NW": 315
    }
    return compass_directions.get(direction, 0)

class ParentRigOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.parent_rig_operator"
    bl_label = "Execute"

    def execute(self, context):
        rig = context.object  # Get the selected object

        # Create an empty object at the world origin
        empty = bpy.data.objects.new("empty", None)
        empty.location = (0, 0, 0)
        bpy.context.collection.objects.link(empty)
        
        # Set the rig to be a child of the empty object
        rig.parent = empty

        # Get the selected animations
        animations = [getattr(context.scene, f"animation_{i}") for i in range(1, context.scene.num_animations + 1)]

        # Get the number of faces and the rotation direction
        num_faces = context.scene.num_faces
        rotation_direction = context.scene.rotation_direction

        # Initialize the start frame for the first animation
        start_frame = 0

        # Create a new NLA track
        rig.animation_data_create()
        track = rig.animation_data.nla_tracks.new()  # Create the track

        # Initialize the INI text
        ini_text = f"Facings={context.scene.num_faces}\n"

        # Initialize the start frame for the first animation
        start_frame = 0

        # Repeat each animation in each direction
        for i, anim in enumerate(animations, start=1):
            if anim:  # Check if an animation is selected
                track.name = anim  # Set the track's name
                angle = 0
                compass_direction = getattr(context.scene, f"compass_direction_{i}")
                if compass_direction == "All":
                    for j in range(num_faces):
                        angle = j * (360 / context.scene.num_faces)
                        end_frame = self.rotate_and_repeat_animation(context, rig, angle, anim, rotation_direction, start_frame, track)
                else:
                    angle = get_compass_angle(compass_direction)
                    end_frame = self.rotate_and_repeat_animation(context, rig, angle, anim, rotation_direction, start_frame, track)

                # Add the animation info to the INI text
                action = bpy.data.actions.get(anim)
                frame_count = int(action.frame_range[1] - action.frame_range[0]) + 1 if action else 0  # Add 1 to the frame count
                ini_entry = getattr(context.scene, f"ini_entry_cw_{i}") if rotation_direction == "CW" else getattr(context.scene, f"ini_entry_ccw_{i}")
                
                # Different output format for infantry
                if rotation_direction == "CCW":
                    ini_text += f"{ini_entry}={start_frame},{frame_count}\n"
                else:
                    ini_text += f"{ini_entry}={frame_count}\n"
                    ini_text += f"Start{ini_entry}={start_frame}\n"
                # Update the start frame for the next animation

                start_frame = end_frame + 1  # Always increment the start frame by 1
                if frame_count > 1:
                    start_frame -= 2  # Subtract 2 from the start frame if frame_count is greater than 1

                # Make sure the track is not muted
                track.mute = False

        # Create a new text block and write the INI text to it
        text_block = bpy.data.texts.new("art_ini")
        text_block.write(ini_text)

        # Report that the output is in the text editor
        self.report({'INFO'}, "Art.ini outputted in text editor")

        return {'FINISHED'}

    def rotate_and_repeat_animation(self, context, rig, angle, anim, rotation_direction, start_frame, track):
        # Repeat the animation
        action = bpy.data.actions.get(anim)
        if action:
            # Calculate the total number of frames used by previous animations
            total_frames_used = 0
            if track.strips:
                total_frames_used = max(strip.frame_end for strip in track.strips)
    
            # Calculate the start frame for the new strip
            new_start_frame = total_frames_used + 1  # Add 1 to create a 1 frame gap
    
            # Create the new strip
            strip = track.strips.new(name=action.name, start=int(new_start_frame), action=action)
    
            # Set the repeat option in the Action Clip to 1
            strip.repeat = 1
    
            # Rotate the parent object and insert a keyframe for each loop
            rig.parent.rotation_euler.z = -math.radians(angle) if rotation_direction == "CW" else math.radians(angle)
            rig.parent.keyframe_insert(data_path="rotation_euler", frame=int(new_start_frame))
    
            # Set the interpolation type to constant for each keyframe
            fcurves = rig.parent.animation_data.action.fcurves
            for fcurve in fcurves:
                if fcurve.data_path == "rotation_euler":
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'CONSTANT'
    
            # Set the extrapolation to 'HOLD_FORWARD'
            strip.extrapolation = 'HOLD_FORWARD'
    
            # Return the end frame of the animation
            return int(strip.frame_end) + 1  # Add 1 to create a 1 frame gap

class AddAnimationOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.add_animation_operator"
    bl_label = "Add Animation"

    def execute(self, context):
        context.scene.num_animations += 1
        
        # Set start frame of the playback/rendering range to 1
        bpy.context.scene.frame_start = 1
       
        # Get the end frame of the last animation strip
        end_frame = 0
        for strip in track.strips:
            end_frame = max(end_frame, strip.frame_end)
       
        # Set end frame of the playback/rendering range to the last frame of the last animation strip
        bpy.context.scene.frame_end = end_frame
        return {'FINISHED'}

class RotateKeyframeOperator(bpy.types.Operator):
    """Rotate selected object"""
    bl_idname = "object.rotate_keyframe_operator"
    bl_label = "Rotate"

    def execute(self, context):
        obj = context.object  # Get the selected object
        num_faces = context.scene.rotation_faces
        rotation_direction = context.scene.rotation_direction

        angle_increment = 360 / num_faces

        for i in range(num_faces):
            angle = i * angle_increment
            obj.rotation_euler.z = -math.radians(angle) if rotation_direction == "CW" else math.radians(angle)
            obj.keyframe_insert(data_path="rotation_euler", frame=i+1)

        return {'FINISHED'}

class ANIM_PT_my_panel(bpy.types.Panel):
    bl_idname = "ANIM_PT_my_panel"
    bl_label = "C&C Anim Addon"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "C&C Anim Addon"

    def draw(self, context):
        layout = self.layout

        # Add UI elements for scaling animations
        layout.label(text="Scale animations if needed:")
        row = layout.row()
        row.prop_search(context.scene, "scale_animation", bpy.data, "actions", text="")
        row.prop(context.scene, "scale_num_frames", text="")
        row.operator("object.scale_animation_operator")

        # Add a button for adding animations
        layout.operator("object.add_animation_operator")

        # Add UI elements for selecting animations
        layout.label(text="Select Animations:")
        for i in range(1, context.scene.num_animations + 1):  # Use num_animations to determine how many to display
            row = layout.row()
            row.prop_search(context.scene, f"animation_{i}", bpy.data, "actions", text="")
            if context.scene.rotation_direction == "CW":
                row.prop(context.scene, f"ini_entry_cw_{i}", text="")
            else:
                row.prop(context.scene, f"ini_entry_ccw_{i}", text="")
            row.prop(context.scene, f"compass_direction_{i}", text="")

        # Add UI elements for specifying the number of faces
        layout.label(text="Number of Facings:")
        layout.prop(context.scene, "num_faces", text="")

        # Add UI elements for choosing the rotation direction
        layout.label(text="Rotation Direction:")
        layout.prop(context.scene, "rotation_direction", text="")

        layout.operator("object.parent_rig_operator")

        # Add UI elements for keyframe rotation
        layout.label(text="Rotate selected object")
        layout.prop(context.scene, "rotation_faces", text="Rotation Facings")
        layout.operator("object.rotate_keyframe_operator")

def register():
    bpy.utils.register_class(ParentRigOperator)
    bpy.utils.register_class(AddAnimationOperator)
    bpy.utils.register_class(RotateKeyframeOperator)
    animation_scaler.register()  # Register the animation_scaler
    bpy.utils.register_class(ANIM_PT_my_panel)

    # Define the properties
    bpy.types.Scene.num_faces = bpy.props.IntProperty(name="Number of Faces", default=8, min=1, max=32)
    bpy.types.Scene.num_animations = bpy.props.IntProperty(name="Number of Animations", default=10, min=1)  # New property
    bpy.types.Scene.rotation_direction = bpy.props.EnumProperty(name="Rotation Direction", items=[("CW", "Clockwise (vehicles)", ""), ("CCW", "CounterClockwise (infantry)", "")])
    bpy.types.Scene.scale_animation = bpy.props.StringProperty(name="Scale Animation")  # New property
    bpy.types.Scene.scale_num_frames = bpy.props.IntProperty(name="Scale Num Frames", default=1, min=1)  # New property
    bpy.types.Scene.rotation_faces = bpy.props.IntProperty(name="Rotation Facings", default=8, min=1, max=32)  # New property for keyframe rotation
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
                ("Die1", "Die1", ""),
                ("Die2", "Die2", ""),
                ("FireUp", "FireUp", ""),
                ("FireProne", "FireProne", ""),
                ("Down", "Down", ""),
                ("Up", "Up", ""),
                ("Deploy", "Deploy", ""),
                ("Deployed", "Deployed", ""),
                ("Undeploy", "Undeploy", ""),
                ("Die3", "Die3", ""),
                ("Die4", "Die4", ""),
                ("Die5", "Die5", ""),
                ("Cheer", "Cheer", ""),
                ("Panic", "Panic", ""),
                ("Paradrop", "Paradrop", ""),
                ("Tread", "Tread", ""),
                ("Swim", "Swim", ""),
                ("WetAttack", "WetAttack", ""),
                ("WetIdle1", "WetIdle1", ""),
                ("WetIdle2", "WetIdle2", ""),
                ("WetDie1", "WetDie1", ""),
                ("WetDie2", "WetDie2", ""),
                ("Fly", "Fly", ""),
                ("FireFly", "FireFly", "")
            ],
            name=f"INI Entries (Infantry) {i}",
            default="Ready" if i == 1 else "Guard" if i == 2 else "Walk" if i == 3 else "Idle1" if i == 4 else "Idle2" if i == 5 else "Prone" if i == 6 else "Crawl"  # Set the default value
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

def unregister():
    bpy.utils.unregister_class(ParentRigOperator)
    bpy.utils.unregister_class(AddAnimationOperator)
    bpy.utils.unregister_class(RotateKeyframeOperator)
    animation_scaler.unregister()  # Unregister the animation_scaler
    bpy.utils.unregister_class(ANIM_PT_my_panel)

    # Delete the properties
    del bpy.types.Scene.num_faces
    del bpy.types.Scene.num_animations  # Delete the new property
    del bpy.types.Scene.rotation_direction
    del bpy.types.Scene.scale_animation  # Delete the new property
    del bpy.types.Scene.scale_num_frames  # Delete the new property
    del bpy.types.Scene.rotation_faces  # Delete the keyframe rotation property
    for i in range(1, 21):  # Delete 20 animation selection properties
        delattr(bpy.types.Scene, f"animation_{i}")
        delattr(bpy.types.Scene, f"frame_count_{i}")  # Delete the frame count property
        delattr(bpy.types.Scene, f"ini_entry_cw_{i}")
        delattr(bpy.types.Scene, f"ini_entry_ccw_{i}")
        delattr(bpy.types.Scene, f"compass_direction_{i}")

if __name__ == "__main__":
    register()

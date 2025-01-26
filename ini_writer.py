import bpy
import math
from .mesh_creator import create_circle_arrow_mesh
from .ini_processor import process_ini_data

class ParentRigOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.parent_rig_operator"
    bl_label = "Execute"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        rig = context.object  # Get the selected object

        # Create the custom mesh and use it as the parent
        obj = create_circle_arrow_mesh()
        if obj is None:
            self.report({'ERROR'}, "Failed to create parent mesh object")
            return {'CANCELLED'}
        
        rig.parent = obj

        # Get the selected animations
        animations = [getattr(context.scene, f"animation_{i}") for i in range(1, context.scene.num_animations + 1)]

        # Get the number of faces and the rotation direction
        num_faces = context.scene.num_faces
        rotation_direction = context.scene.rotation_direction

        # Initialize the start frame for the first animation
        start_frame = 0
        previous_loop_clip = False

        # Create a new NLA track
        rig.animation_data_create()
        track = rig.animation_data.nla_tracks.new()  # Create the track
        track.is_solo = True  # Ensure the NLA track is the top layer

        # Initialize the INI text
        ini_text = f"Facings={context.scene.num_faces}\n"

        # Variable to track the end frame of the last strip
        last_end_frame = 0

        # Repeat each animation in each direction
        for i, anim in enumerate(animations, start=1):
            if anim:  # Check if an animation is selected
                track.name = anim  # Set the track's name
                angle = 0
                compass_direction = getattr(context.scene, f"compass_direction_{i}")
                loop_clip = getattr(context.scene, f"loop_clip_{i}")
                
                # Store the initial start frame for the current animation
                initial_start_frame = start_frame
                
                if compass_direction == "All":
                    for j in range(num_faces):
                        angle = j * (360 / context.scene.num_faces)
                        end_frame = self.rotate_and_repeat_animation(context, rig, angle, anim, rotation_direction, start_frame, track, loop_clip)
                        # Increment start_frame for next strip based on loop_clip status
                        start_frame = end_frame + (0 if loop_clip else 1)
                        last_end_frame = max(last_end_frame, end_frame)
                else:
                    angle = get_compass_angle(compass_direction)
                    end_frame = self.rotate_and_repeat_animation(context, rig, angle, anim, rotation_direction, start_frame, track, loop_clip)
                    # Increment start_frame for next strip based on loop_clip status
                    start_frame = end_frame + (0 if loop_clip else 1)
                    last_end_frame = max(last_end_frame, end_frame)

                # Add the animation info to the INI text
                action = bpy.data.actions.get(anim)
                frame_count = int(action.frame_range[1] - action.frame_range[0]) + 1 if action else 0  # Add 1 to the frame count
                ini_entry = getattr(context.scene, f"ini_entry_cw_{i}") if rotation_direction == "CW" else getattr(context.scene, f"ini_entry_ccw_{i}")
                
                # Different output format for infantry
                if rotation_direction == "CCW":
                    if compass_direction == "All":
                        ini_text += f"{ini_entry}={initial_start_frame},{frame_count}\n"  # Correct INI sequence
                    else:
                        if ini_entry not in ["Die1", "Die2"]:
                            ini_text += f"{ini_entry}={initial_start_frame},{frame_count},0,{compass_direction}\n"  # Correct INI sequence with compass direction
                        else:
                            ini_text += f"{ini_entry}={initial_start_frame},{frame_count}\n"  # Correct INI sequence without 3rd and 4th values for Die1 and Die2
                else:
                    ini_text += f"{ini_entry}={frame_count}\n"
                    ini_text += f"Start{ini_entry.replace('Frames', 'Frame')}={initial_start_frame}\n"  # Correct INI sequence
                
                previous_loop_clip = loop_clip

                # Make sure the track is not muted
                track.mute = False

        # Process the INI data to complete the sequence if rotation direction is CCW
        if rotation_direction == "CCW":
            processed_ini_text, added_keys = process_ini_data(ini_text)
        else:
            processed_ini_text = ini_text

        # Create a new text block and write the processed INI text to it
        text_block = bpy.data.texts.new("art_ini")
        text_block.write(processed_ini_text)

        # Set the playback range
        context.scene.frame_start = 0
        context.scene.frame_end = last_end_frame

        # Report that the output is in the text editor
        self.report({'INFO'}, "Art.ini outputted in text editor")

        return {'FINISHED'}

    def rotate_and_repeat_animation(self, context, rig, angle, anim, rotation_direction, start_frame, track, loop_clip):
        # Repeat the animation
        action = bpy.data.actions.get(anim)
        if action:
            # Calculate the start frame for the new strip
            new_start_frame = start_frame
            
            # Ensure there is space for the new strip
            while any(strip.frame_start <= new_start_frame < strip.frame_end for strip in track.strips):
                new_start_frame += 1  # Move the start frame to the right
    
            # Create the new strip
            strip = track.strips.new(name=action.name, start=int(new_start_frame), action=action)
    
            # Set the repeat option in the Action Clip to 1
            strip.repeat = 1
    
            # Rotate the parent object and insert a keyframe for each loop
            if rig.parent is not None:
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
    
                # Calculate the end frame of the strip
                end_frame = int(strip.frame_end)

                # Return the end frame of the animation
                return end_frame
            else:
                self.report({'ERROR'}, "Parent object is not set")
                return start_frame

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
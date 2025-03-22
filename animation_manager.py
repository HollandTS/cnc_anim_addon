import bpy
from .ini_processor import process_ini_data

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

class ANIM_PT_animation_panel(bpy.types.Panel):
    bl_idname = "ANIM_PT_animation_panel"
    bl_label = "Animation Manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AnimFacer CnC Addon"
    bl_order = 3  # This ensures it appears after the scale animations panel

    def draw(self, context):
        layout = self.layout

        # Section for adding animations
        box = layout.box()
        box.operator("object.add_animation_operator")

        # Section for selecting animations
        box = layout.box()
        box.label(text="Select Animations:")
        for i in range(1, context.scene.num_animations + 1):
            row = box.row()
            row.prop_search(context.scene, f"animation_{i}", bpy.data, "actions", text="")
            if context.scene.rotation_direction == "CW":
                row.prop(context.scene, f"ini_entry_cw_{i}", text="")
            else:
                row.prop(context.scene, f"ini_entry_ccw_{i}", text="")
            row.prop(context.scene, f"compass_direction_{i}", text="")
            row.prop(context.scene, f"loop_clip_{i}", text="Loop Clip")

        # Execute and Undo buttons
        box = layout.box()
        row = box.row()
        row.scale_y = 1.5
        row.operator("object.parent_rig_operator")

        box = layout.box()
        row = box.row(align=True)
        row.label(text="Undo execution:")
        row.operator("object.undo_execution", text="Remove", icon='CANCEL')

def register():
    bpy.utils.register_class(AddAnimationOperator)
    bpy.utils.register_class(UndoExecutionOperator)
    bpy.utils.register_class(ANIM_PT_animation_panel)

    # Define the properties
    bpy.types.Scene.num_animations = bpy.props.IntProperty(name="Number of Animations", default=10, min=1)

    # Create animation selection properties
    for i in range(1, 21):
        setattr(bpy.types.Scene, f"animation_{i}", bpy.props.StringProperty(name=f"Animation {i}"))
        setattr(bpy.types.Scene, f"frame_count_{i}", bpy.props.IntProperty(name=f"Frame Count {i}"))
        setattr(bpy.types.Scene, f"ini_entry_cw_{i}", bpy.props.EnumProperty(
            items=[
                ("StandingFrames", "StandingFrames", ""),
                ("WalkFrames", "WalkFrames", ""),
                ("DeathFrames", "DeathFrames", ""),
                ("FiringFrames", "FiringFrames", ""),
                ("IdleFrames", "IdleFrames", "")
            ],
            name=f"INI Entries (Vehicles) {i}",
            default="StandingFrames" if i == 1 else "WalkFrames" if i == 2 else "DeathFrames" if i == 3 else "FiringFrames" if i == 4 else "IdleFrames"
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
            default="Ready" if i == 1 else "Guard" if i == 2 else "Walk" if i == 3 else "Idle1" if i == 4 else "Idle2" if i == 5 else "Prone" if i == 6 else "Crawl" if i == 7 else "FireUp" if i == 8 else "FireProne" if i == 9 else "Die1"
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
            default="All"
        ))
        setattr(bpy.types.Scene, f"loop_clip_{i}", bpy.props.BoolProperty(name=f"Loop Clip {i}", default=False))

def unregister():
    bpy.utils.unregister_class(AddAnimationOperator)
    bpy.utils.unregister_class(UndoExecutionOperator)
    bpy.utils.unregister_class(ANIM_PT_animation_panel) 
import bpy
import math

def create_circle_arrow_mesh():
    # Parameters for the circle
    radius = 1.0
    num_segments = 32
    rotation_angle = math.radians(-135)  # Rotate -135 degrees on Z-axis

    # Function to rotate a point around the Z-axis
    def rotate_z(x, y, angle):
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        x_new = x * cos_theta - y * sin_theta
        y_new = x * sin_theta + y * cos_theta
        return x_new, y_new

    # Create a new mesh and object
    mesh = bpy.data.meshes.new("CircleArrowMesh")
    obj = bpy.data.objects.new("CircleArrow", mesh)

    # Link object to the scene
    bpy.context.collection.objects.link(obj)

    # Generate and rotate circle vertices
    vertices = [
        rotate_z(
            math.cos(2 * math.pi * i / num_segments) * radius,
            math.sin(2 * math.pi * i / num_segments) * radius,
            rotation_angle
        ) + (0.0,)  # Add Z-coordinate
        for i in range(num_segments)
    ]

    # Arrow parameters
    arrow_base_width = 0.3  # Width of the arrow's base
    arrow_tip_width = 0.15  # Width of the arrow's tip
    arrow_length = 0.4  # Total length of the arrow
    arrow_offset = -1.2  # Offset position for the arrow

    # Arrow vertices (defining a triangular tip with a base)
    arrow_tip_vertices = [
        rotate_z(arrow_base_width / 2, arrow_offset, rotation_angle) + (0.0,),
        rotate_z(-arrow_base_width / 2, arrow_offset, rotation_angle) + (0.0,),
        rotate_z(0.0, arrow_offset - arrow_length, rotation_angle) + (0.0,)
    ]

    vertices.extend(arrow_tip_vertices)

    # Edges for the circular part
    edges = [(i, (i + 1) % num_segments) for i in range(num_segments)]

    # Add arrow-specific edges
    arrow_start_index = num_segments
    edges.extend([
        (arrow_start_index, arrow_start_index + 1),  # Base of arrow
        (arrow_start_index + 1, arrow_start_index + 2),  # Base to tip
        (arrow_start_index + 2, arrow_start_index)  # Tip to base
    ])

    # Create the mesh data
    mesh.from_pydata(vertices, edges, [])

    # Update the mesh
    mesh.update()

    return obj  # Return the created mesh object
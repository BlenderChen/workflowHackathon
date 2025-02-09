"""
import sys
import subprocess

python_exe = sys.executable
subprocess.run([python_exe, "-m", "pip", "install", "pygame"])
"""


import bpy
import pygame
import time

# Initialize pygame and joystick
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Detected controller: {joystick.get_name()}")

# Blender camera reference
camera = bpy.data.objects["Camera"]  # Ensure your camera is named "Camera"

# Sensitivity and movement recording variables
sensitivity = 0.1
recording = False
movement_data = []  # Stores (timestamp, position, rotation) tuples

# Function to process joystick input
def get_joystick_input():
    pygame.event.pump()

    # Joystick axes
    left_x = joystick.get_axis(0)  # Left stick X
    left_y = joystick.get_axis(1)  # Left stick Y
    right_x = joystick.get_axis(3)  # Right stick X
    right_y = joystick.get_axis(4)  # Right stick Y

    # Joystick button (A button - index 0)
    button_a = joystick.get_button(0)  

    return left_x, left_y, right_x, right_y, button_a

# Function to convert movement data into a natural language description
def generate_movement_description(movement_data):
    description = "The camera moves in the following way:\n"
    
    for i in range(1, len(movement_data)):
        prev_time, prev_pos, prev_rot = movement_data[i - 1]
        curr_time, curr_pos, curr_rot = movement_data[i]

        time_diff = curr_time - prev_time
        move_x = curr_pos[0] - prev_pos[0]
        move_y = curr_pos[1] - prev_pos[1]
        move_z = curr_pos[2] - prev_pos[2]

        rotate_x = curr_rot[0] - prev_rot[0]
        rotate_y = curr_rot[1] - prev_rot[1]
        rotate_z = curr_rot[2] - prev_rot[2]

        # Generate description based on movement
        if abs(move_x) > 0.01:
            description += f"- Moves {'right' if move_x > 0 else 'left'} by {abs(move_x):.2f} units in {time_diff:.2f} seconds.\n"
        if abs(move_y) > 0.01:
            description += f"- Moves {'forward' if move_y < 0 else 'backward'} by {abs(move_y):.2f} units in {time_diff:.2f} seconds.\n"
        if abs(move_z) > 0.01:
            description += f"- Moves {'up' if move_z > 0 else 'down'} by {abs(move_z):.2f} units in {time_diff:.2f} seconds.\n"

        if abs(rotate_x) > 0.01:
            description += f"- Rotates {'up' if rotate_x > 0 else 'down'} by {abs(rotate_x):.2f} degrees.\n"
        if abs(rotate_y) > 0.01:
            description += f"- Rotates {'left' if rotate_y < 0 else 'right'} by {abs(rotate_y):.2f} degrees.\n"
        if abs(rotate_z) > 0.01:
            description += f"- Rotates {'clockwise' if rotate_z > 0 else 'counterclockwise'} by {abs(rotate_z):.2f} degrees.\n"

    return description

# Main recording loop
def record_movements():
    global recording, movement_data

    print("Press 'A' button to start recording...")
    
    while True:
        left_x, left_y, right_x, right_y, button_a = get_joystick_input()

        # Toggle recording on button press
        if button_a:
            recording = not recording
            if recording:
                print("Recording started!")
                movement_data = []  # Reset movement data
            else:
                print("Recording stopped!")
                description = generate_movement_description(movement_data)
                print("\nGenerated Description:\n", description)
                return description  # Return the generated description
        
        if recording:
            # Apply movement to camera
            camera.location.x += left_x * sensitivity
            camera.location.y -= left_y * sensitivity
            camera.rotation_euler[2] += right_x * sensitivity
            camera.rotation_euler[0] += right_y * sensitivity

            # Save movement data
            movement_data.append((
                time.time(),
                (camera.location.x, camera.location.y, camera.location.z),
                (camera.rotation_euler[0], camera.rotation_euler[1], camera.rotation_euler[2])
            ))

        pygame.time.wait(50)  # Prevent CPU overuse

# Run the function
description = record_movements()

# Save the description to a text file for LLM input
with open("camera_movement.txt", "w") as file:
    file.write(description)

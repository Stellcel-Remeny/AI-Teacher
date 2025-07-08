#
# Camera backend stuff
# Copyright (C) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher.resources import functions as f
from ai_teacher.resources import shared
from typing import Union
import cv2
import platform

# ---[ Variables ]--- #
# Items in the following list are the ones which get displayed on camera window
user_instructions: list[str] = [
    "Turn your head to your left",
    "Turn your head to your right",
    "Turn your head down a little (circles must be visible)",
    "Turn your head up a little (circles must be visible)",
    "Look straight into your camera",
    "Look dead center into your monitor",
    "END"
]

# Items in the following list are the keys which get added to user config ini file
user_instruction_ini_setting: list[str] = [
    "head_turn_left",
    "head_turn_right",
    "head_down",
    "head_up",
    "head_straight",
    "head_straight_camera"
]

# This variable keeps track of which instruction it's currently at
user_instruction_count: int = 0

def list_cameras() -> list[tuple[int, str]]:
    """
    List available cameras.
    """
    cameras: list[tuple[int, str]] = []

    if platform.system() == "Windows":
        # Windows
        from pygrabber.dshow_graph import FilterGraph
        graph = FilterGraph()
        devices = graph.get_input_devices()
        for i, name in enumerate(devices):
            cameras.append((i, name))
    else:
        # Linux, mac
        i = 0
        fails = 0
        while fails < 3:  # stop after 3 failed indices in a row
            cap = cv2.VideoCapture(i)
            f.dbg(f"Trying capture: {cap}")
            if check_camera(cap):
                cameras.append((i, f"Camera {i}"))
                fails = 0
            else:
                fails += 1
            cap.release()
            i += 1

    f.dbg(f"Available cameras: {cameras}")
    return cameras

def check_camera(camera: "cv2.VideoCapture") -> bool:
    """
    Check if the camera is working
    """
    # Check if it can read a frame
    if not camera.isOpened():
        f.dbg("Error: Camera is not opened.")
        return False
    
    ret, frame = camera.read()
    if not ret or frame is None: # type: ignore
        f.dbg("Error: Could not read from camera.")
        return False
    
    f.dbg("Camera check successful.")
    return True

def capture_face_points(left_eye: list[float], right_eye: list[float], nose: list[float]) -> str:
    """
    Stores the 3D coordinates of facial landmarks (left eye, right eye, and nose)
    for training or calibration purposes.

    Args:
        left_eye (list[float]): [x, y, z] coordinates of the left iris.
        right_eye (list[float]): [x, y, z] coordinates of the right iris.
        nose (list[float]): [x, y, z] coordinates of the nose tip.

    Returns:
        str: Next instruction to be displayed
    """
    global user_instruction_count
    f.dbg(f"Capturing the following (down) coordinates into master key: {user_instruction_ini_setting[user_instruction_count]}")
    f.dbg("LEFT:", left_eye)
    f.dbg("RIGHT:", right_eye)
    f.dbg("NOSE:", nose)
    
    key = user_instruction_ini_setting[user_instruction_count]
    points = {'left': left_eye, 'right': right_eye, 'nose': nose}
    
    for name, coords in points.items():
        f.dbg(name.upper(), coords)
        for axis, value in zip('xyz', coords):
            f.update_ini(shared.user_config_file, 'Facemarks', f"{key}_{name}_{axis}", value)
    
    user_instruction_count += 1
    return user_instructions[user_instruction_count]
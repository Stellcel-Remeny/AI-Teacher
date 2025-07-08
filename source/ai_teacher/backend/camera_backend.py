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

def list_cameras() -> list[tuple[int, str]]:
    """
    List available cameras.
    """
    cameras: list[tuple[int, str]] = []

    if platform.system() == "Windows":
        from pygrabber.dshow_graph import FilterGraph
        graph = FilterGraph()
        devices = graph.get_input_devices()
        for i, name in enumerate(devices):
            cameras.append((i, name))
    else:
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

def capture_face_points(left_eye, right_eye, nose) -> None:
    print("LEFT:", left_eye)
    print("RIGHT:", right_eye)
    print("NOSE:", nose)
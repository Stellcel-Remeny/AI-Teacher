#
# Camera backend stuff
# Copyright (C) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher import function as f
from ai_teacher.global_variables import *
from PIL import Image, ImageTk
from typing import Union
import cv2

def init(camera_index: int, width: int = 640, height: int = 480) -> Union[bool, cv2.VideoCapture]:
    """
    Initialize the video capturer.
    """
    camera = cv2.VideoCapture(camera_index)
    
    if check_camera(camera) is False:
        f.dbg(f"Error: Could not open camera: {camera}")
        f.dbg(f"Camera index {camera_index} couldn't be opened.")
        return False
    
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    f.dbg(f"Camera initialized with resolution: {width}x{height}")
    return camera

def list_cameras() -> list:
    """
    List available cameras.
    """
    from pygrabber.dshow_graph import FilterGraph
    graph = FilterGraph()
    devices = graph.get_input_devices()
    cameras = []
    for i, name in enumerate(devices):
        cameras.append((i, name))
    
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
    if not ret or frame is None:
        f.dbg("Error: Could not read from camera.")
        return False
    
    f.dbg("Camera check successful.")
    return True
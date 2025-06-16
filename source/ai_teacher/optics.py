#
# Camera backend stuff
# Copyright (C) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher import function as f
from ai_teacher.global_variables import *
from typing import Union
import cv2

def init(camera_index: int, width: int = 640, height: int = 480) -> Union[bool, cv2.VideoCapture]:
    """
    Initialize the video capturer.
    """
    camera = cv2.VideoCapture(camera_index, get_camera_backend())
    
    if check_camera(camera) is False:
        f.dbg(f"Error: Could not open camera: {camera}")
        f.dbg(f"Camera index {camera_index} couldn't be opened.")
        return False
    
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    f.dbg(f"Camera initialized with resolution: {width}x{height}")
    return camera

def get_camera_backend():
    """
    Get the appropriate camera backend based on the operating system.
    """
    system = platform.system()
    if system == "Windows":
        return cv2.CAP_DSHOW
    elif system == "Linux":
        return cv2.CAP_V4L2  # default and best choice for Linux
    elif system == "Darwin":  # macOS
        return cv2.CAP_AVFOUNDATION
    else:
        return 0  # fallback to default

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

def write_image(camera: "cv2.VideoCapture", save_path: str) -> bool:
    """
    Capture an image from the camera and save it to the specified path.
    """
    ret, frame = camera.read()
    if ret:
        cv2.imwrite(save_path, frame)
        f.dbg(f"Image captured and saved to {save_path}")
        return True
    else:
        f.dbg(f"Failed to capture image: ret value = {ret}")
        return False
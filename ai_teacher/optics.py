#
# This python file deals with anything camera related
# Copyright (C) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher import function as f
from ai_teacher.global_variables import *
import cv2
from PIL import Image, ImageTk

def init(width: int = 640, height: int = 480) -> "cv2.VideoCapture":
    """
    Initialize the video capturer.
    """
    camera = cv2.VideoCapture(0)
    
    if check_camera(camera) is False:
        f.dbg(f"Error: Could not open camera: {camera}")
        f.quit(1, "Camera initialization failed.")
    
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    f.dbg(f"Camera initialized with resolution: {width}x{height}")
    return camera

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
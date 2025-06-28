#
# NEW: Python face detection using Google MediaPipe
# For Remeny AI-Teacher
#

# ---[ Libraries ]--- #
from ai_teacher.resources import functions as f
from ai_teacher.resources import shared
from ai_teacher.backend import camera_backend
from ai_teacher.gui import gui

import customtkinter as ctk # type: ignore
import cv2
import mediapipe as mp # type: ignore
from PIL import Image, ImageTk # type: ignore

mp_face_mesh = mp.solutions.face_mesh

def init(win: "gui.app") -> None:
    win.root.title("Remeny AI Teacher - Camera Trainer")
    gui.banner(win.main, "Camera selector", "Select a camera to use with MediaPipe.")
    action_buttons = gui.ActionBar(
        win.root,
        buttons=(("Next", gui.not_implemented), ("Cancel", gui.quit))
    ).get()[1]
    
    action_buttons["Next"].configure(state="disabled") # type: ignore
    
    # Get the available cameras.
    # User should be able to select which one to use.
    cameras = camera_backend.list_cameras()
    if not cameras:
        # No cameras are available
        f.quit(1, "No cameras are available. Check if you have permissions, or connect a camera if you don't have one.")
        
    camera_names = [name for (_, name) in cameras]
    
    # Add the camera selector
    combobox_cam_selector = gui.CTkLabeledComboBox(win.main, "Use camera:", camera_names)
    combobox_cam_selector.grid(padx=50, pady=20, sticky="w") # type: ignore
    
    # Textboxes
    help_label = ctk.CTkLabel(win.main, text="/\\\n|\nSelect a camera from the dropdown above.\nYou should see another window pop up with the camera feed.")
    help_label.grid(padx=10, pady=0, sticky="w") # type: ignore
    win.root.mainloop()
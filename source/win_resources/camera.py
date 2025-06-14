#
# Python camera GUI
# Copyright (C) 2025 Remeny
#

import customtkinter as ct
from ai_teacher import optics
from ai_teacher import gui
import cv2
from PIL import Image, ImageTk

"""
def open_camera():

    # Capture the video frame by frame
    _, frame = cam.read()

    # Convert image from one color space to other
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    # Capture the latest frame and transform to image
    captured_image = Image.fromarray(opencv_image)

    # Convert captured image to photoimage
    photo_image = ImageTk.PhotoImage(image=captured_image)

    # Displaying photoimage in the label
    label_widget.photo_image = photo_image

    # Configure image in the label
    label_widget.configure(image=photo_image)

    # Repeat the same process after every 10 seconds
    label_widget.after(10, open_camera)

def init(win: "ct.CTk") -> None:
    gui.reinit(win,"Camera Calibrator", 800, 600)
    win.config(bg="#176dee")  # Set a light background color
    global cam
    cam = optics.init(320,240)  # Initialize the camera
    global label_widget
    label_widget = ct.Label(win)
    label_widget.pack()
    button1 = ct.Button(win, text="Open Camera", command=open_camera)
    button1.pack()
    win.mainloop()
"""

def init(win: "ct.CTk") -> None:
    gui.reinit(win, "Remeny AI Teacher - Camera Trainer")
    gui.banner(win, "Camera Trainer", "Select a camera to train the AI teacher.")
    cameras = optics.list_cameras()
    win.mainloop()
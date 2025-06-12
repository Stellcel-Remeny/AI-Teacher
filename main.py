# AI Teacher Application
# Copyright (C) 2025 Remeny
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####
#
# Introduction:
# ----------------
#
# The AI Teacher application utilizes a free AI system API
# with given instructions in 'instructions.txt' file.
# The instructions will be the first message sent to the AI
# System, followed by acquiring information about the user.
#
# NOTE: Use at your own risk! We, Remeny, do not seek
# to collect ANY of your personally identifiable information
# nor give it to others. The AI Systems utilized are out of
# range for our control. As a result, YOU (or anyone using
# this product) acknowledges that YOU consent to any data
# which may be taken for use by the Artifical Intelligence
# System.
#
# ++ Remeny, 28th May 2025 9:46PM ++ #
#

# ---[ Libraries ]--- #
from ai_teacher import speech
from ai_teacher import function as f
from ai_teacher.global_variables import *
# For GUI application
import tkinter as tk
from ai_teacher import gui
# For Camera
from ai_teacher import optics
import cv2
from PIL import Image, ImageTk

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

# ---[ Main Initialization ]--- #
def main():
    f.init()
    # Window initialization
    win = gui.init() # Our main application window
    global cam
    cam = optics.init(800,600)  # Initialize the camera
    global label_widget
    label_widget = tk.Label(win)
    label_widget.pack()
    button1 = tk.Button(win, text="Open Camera", command=open_camera)
    button1.pack()
    win.mainloop()
    f.dbg("Window is closed.")
    f.quit(0)

if __name__ == "__main__":
    main()

#
# AI Teacher Application
# Copyright (C) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher.resources import shared
from ai_teacher.resources import functions as f
from ai_teacher import gui

import customtkinter as ctk

# ---[ Main Initialization ]--- #
def main():
    f.init()
    # Window initialization
    win = gui.gui.mainapp() # Our main application window
    gui.camera.init(win)  # Initialize the camera
    f.dbg("Window is closed.")
    f.quit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        f.quit(130, "Quitting on keyboard interruption")
    except Exception as e:
        print("Exception:", e)

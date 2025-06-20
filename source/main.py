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
from source.ai_teacher.shared_variables import *
# For GUI application
import customtkinter as ctk
from ai_teacher import gui
# For Camera
from win_resources.camera import cam_init

# ---[ Main Initialization ]--- #
def main():
    f.init()
    # Window initialization
    win = gui.mainapp() # Our main application window
    cam_init(win)  # Initialize the camera
    win.main.mainloop()
    f.dbg("Window is closed.")
    f.quit(0)

if __name__ == "__main__":
    main()

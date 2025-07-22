#
# AI Teacher Application
# Copyright (C) 2025 Remeny
#

# ---[ Libraries ]--- #
import os
import sys
import tkinter as tk

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

from ai_teacher.resources import shared
from ai_teacher.resources import functions as f
from ai_teacher import gui

# ---[ Main Program Entry ]--- #
def main():
    # Early init
    f.init()
    # Login, license and session type
    from ai_teacher.backend.login import login
    from ai_teacher.resources.notices import show_notices
    
    login()   
    show_notices(f"{shared.app_dir}/text/DISCLAIMER.txt", "GPLv3")
    shared.main_app = gui.gui.app() # Our main application window
    shared.session_type = gui.login.ask_session(shared.main_app)
    f.dbg(f"Session type: {shared.session_type}")
    
    # Camera trainer
    gui.camera.camera_trainer(shared.main_app)  # Start mediapipe and the user webcam
    f.dbg("Window is closed.")
    f.quit(0)

if __name__ == "__main__":
    import traceback
    
    def handle_exception(exc_type, exc_value, exc_traceback): # type: ignore
        if issubclass(exc_type, KeyboardInterrupt):
            f.quit(130, "KeyboardInterrupt", dialog=False)
        else:
            tb = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)) # type: ignore
            print("[Global Exception Hook]", tb)
            f.quit(1, f"Unhandled Exception:\n{tb}")

    sys.excepthook = handle_exception
    
    def tk_callback_exception_handler(exc_type, exc_value, exc_traceback): # type: ignore
        tb = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)) # type: ignore
        print("[Tkinter Exception]", tb)
        f.quit(1, f"Tkinter Callback Exception:\n{tb}")

    tk.Tk.report_callback_exception = staticmethod(tk_callback_exception_handler) # type: ignore
    
    try:
        main()
    except KeyboardInterrupt:
        f.quit(130, "Quitting on keyboard interruption", dialog=False)
    except Exception as e:
        f.dbg("Error traceback:")
        f.dbg(traceback.format_exc())
        f.quit(1, f"Exception: {str(e)}")

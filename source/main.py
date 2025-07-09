#
# AI Teacher Application
# Copyright (C) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher.resources import shared
from ai_teacher.resources import functions as f
from ai_teacher import gui

import sys
import tkinter as tk

# ---[ Main Initialization ]--- #
def main():
    f.init()
    # Window initialization
    shared.main_app = gui.gui.app() # Our main application window
    gui.camera.camera_trainer()  # Start mediapipe and the user webcam
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

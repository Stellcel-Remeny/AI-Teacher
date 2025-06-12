#
# This file deals with anything GUI related
# Copyright (c) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher import function as f
import tkinter as tk
from tkinter import messagebox

def init() -> "tk.Tk":
    """
    Initialize the main window for the AI Teacher application.
    This function sets up the main window, including its title, size, and icon.
    It also initializes the menu bar and status bar.
    """

    win = tk.Tk()
    win.title("Remeny AI Teacher Application")
    win.geometry("800x600")
    win.iconbitmap("resources/icon.ico")
    win.resizable(True, True)
    win.config(bg="#176dee")  # Set a light background color
    f.dbg(f"Window is initialized.")
    
    return win

def error(msg: str) -> None:
    """
    Display an error message in a pop-up window.
    
    Args:
        msg (str): The error message to display.
    """
    messagebox.showerror("Error", "An error occured: " + msg)
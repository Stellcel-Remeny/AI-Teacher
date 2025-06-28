#
# This file deals with anything simple GUI related
# Copyright (c) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher.resources import functions as f
from ai_teacher.resources import shared

from tkinter import messagebox
from typing import Callable
from typing import Union

import tkinter as tk
import customtkinter as ctk
import os
import platform

class app:
    """
    Application class for Remeny AI Teacher GUI.
    """
    def __init__(self, title: str = "Remeny AI Teacher", width: int = 800, height: int = 600):
        # Theme settings
        theme: str = (
            shared.user_config.get('Main', 'theme', fallback="system").lower()
            if shared.user_config is not None else
            "system"
        )
        if theme in ("auto", "system"):
            ctk.set_appearance_mode("system")
        elif theme in ("light", "dark"):
            ctk.set_appearance_mode(theme)
        else:
            f.dbg("Invalid theme= setting in configuration.ini, defaulting to system theme")
            warn("Invalid theme= setting in configuration.ini")
            ctk.set_appearance_mode("system")
        
        # basic stuff
        self.root = ctk.CTkToplevel(shared.root_app)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        if platform.system() == "Windows":
            self.root.iconbitmap(f"{shared.app_dir}/media/icons/icon.ico")
        else:
            xbm_path = f"{shared.app_dir}/media/icons/icon-0.xbm"
            if os.path.exists(xbm_path):
                self.root.iconbitmap(f"@{xbm_path}")
            else:
                print("[Info] XBM icon not found, skipping window icon.")
        
        self.root.resizable(True, True)
        # Map close button to quit()
        self.root.protocol("WM_DELETE_WINDOW", lambda: quit())
        # Configure the grid to expand
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        # Scrollbar main frame
        self.main = ctk.CTkScrollableFrame(
            self.root,
            fg_color=("#e5e5e5", "#1a1a1a")  # Light theme, Dark theme
        )
        self.main.grid(row=0, column=0, sticky="nsew")
        self.main.pack_propagate(False)  # Prevent content from shrinking the frame
        f.dbg(f"Initialized new app with title: '{title}'")

def init(title: str = "Remeny AI Teacher MAIN", width: int = 0, height: int = 0) -> None:
    """
    Initializes the GUI application.
    """
    f.dbg("Initializing GUI application...")
    shared.root_app = ctk.CTk()
    shared.root_app.title(title)
    shared.root_app.geometry(f"{width}x{height}")
    shared.root_app.withdraw()  # Hide the root window
    f.dbg("GUI application initialized.")

def error(msg: str, title: str = "Error") -> None:
    """
    Display an error message in a pop-up window.
    
    Args:
        msg (str): The error message to display.
        title (str = "Error"): Window title
    """
    messagebox.showerror(title, f"An error occured: {msg}")
    
def warn(msg: str, title: str = "Warning!") -> None:
    """
    Display a warning
    
    Args:
        msg (str): The error message to display.
        title (str = "Error"): Window title
    """
    messagebox.showwarning(title, f"Warning: {msg}")

def clear_window(win: "ctk.CTk") -> None:
    """
    Clears all stuff inside a window
    """
    for widget in win.winfo_children():
        widget.quit()
    f.dbg("Cleared window")
    
def clear_frame(frame: ctk.CTkFrame) -> None:
    """
    Clears all widgets inside the given frame.
    """
    for widget in frame.winfo_children():
        widget.destroy()
    f.dbg("Cleared frame")
    
def banner(win: "ctk.CTkFrame", heading: str, text: str, height: int = 65) -> None:
    """
    Adds some user-friendly text at the top, expanding horizontally with window resize.
    """
    win.grid_columnconfigure(0, weight=1)

    frame = ctk.CTkFrame(master=win, height=height)
    frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    frame.pack_propagate(False)  # Prevent content from shrinking the frame

    label_heading = ctk.CTkLabel(
        master=frame,
        text=heading,
        font=ctk.CTkFont(size=20, weight="bold"),
        justify="left"
    )
    label_heading.pack(anchor="w", padx=14, pady=(10, 0))  # Top padding only

    label_text = ctk.CTkLabel(
        master=frame,
        text=text,
        font=ctk.CTkFont(size=14),
        justify="left"
    )
    label_text.pack(anchor="w", padx=16, pady=(0, 5))  # Bottom padding only

    f.dbg(f"Added banner with heading: '{heading}' and text: '{text}'")
    
def action_bar(
    win: Union[ctk.CTk, ctk.CTkScrollableFrame, ctk.CTkFrame],
    buttons: tuple[tuple[str, Callable], ...]
) -> tuple[ctk.CTkFrame, dict[str, ctk.CTkButton]]:
    """
    Adds a horizontal action bar with buttons at the bottom of the window.

    Returns:
        A tuple of (action_frame, button_dict)
    """
    win.rowconfigure(0, weight=1)
    win.rowconfigure(1, weight=0)
    win.columnconfigure(0, weight=1)

    action_frame = ctk.CTkFrame(master=win, height=40, corner_radius=10)
    action_frame.grid(row=1, column=0, sticky="ew")
    action_frame.grid_propagate(False)

    button_refs = {}

    for text, command in buttons:
        button = ctk.CTkButton(master=action_frame, text=text, command=command)
        button.pack(side="right", padx=(5, 5), pady=5)
        button_refs[text] = button  # Save reference

    f.dbg(f"Added action bar with buttons: {buttons}")
    return action_frame, button_refs

class CTkLabeledComboBox(ctk.CTkFrame):
    def __init__(
        self,
        master: Union[ctk.CTkFrame, ctk.CTkScrollableFrame],
        text: str,
        values: list[str],
        default_value: str = "",
        width: int = 200,
        height: int = 30,   
        *args, **kwargs
    ):
        super().__init__(master=master, width=width, height=height, *args, **kwargs)
        self.label = ctk.CTkLabel(self, text=text)
        self.label.pack(side="left", padx=5, pady=5)

        self.combobox = ctk.CTkComboBox(self, values=values, width=width - 50)
        self.combobox.pack(side="left", padx=5, pady=5)
        self.combobox.set(default_value)

    def get(self) -> str:
        return self.combobox.get()

    def set(self, value: str):
        self.combobox.set(value)

def quit() -> None:
    """
    Asks if the user wants to quit the application.
    """
    result = messagebox.askquestion("Confirm Action", "Are you sure you want to quit?")
    if result == "yes":
        f.dbg("GUI: Quitting application...")
        try:
            if tk._default_root and tk._default_root.winfo_exists():
                tk._default_root.destroy()
        except Exception as e:
            f.dbg(f"Exception during quit: {e}")
        f.quit(0)
        
def not_implemented() -> None:
    messagebox.showinfo("Not Implemented Yet", "This feature is not implemented yet.")
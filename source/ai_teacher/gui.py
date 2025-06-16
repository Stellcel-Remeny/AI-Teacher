#
# This file deals with anything simple GUI related
# Copyright (c) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher import function as f
import customtkinter as ctk
from tkinter import messagebox

class mainapp:
    """
    Main application class for Remeny AI Teacher GUI.
    This class is responsible for initializing the main window.
    """
    def __init__(self, title: str = "Remeny AI Teacher", width: int = 800, height: int = 600):
        # basic stuff
        self.root = ctk.CTk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.iconbitmap("resources/icon.ico")
        self.root.resizable(True, True)
        # Configure the grid to expand
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        # Scrollbar main frame
        self.main = ctk.CTkScrollableFrame(self.root, fg_color="#1a1a1a")
        self.main.grid(row=0, column=0, sticky="nsew")
        self.main.pack_propagate(False)  # Prevent content from shrinking the frame
        f.dbg(f"Initialized new main app with title: '{title}'")

def error(msg: str) -> None:
    """
    Display an error message in a pop-up window.
    
    Args:
        msg (str): The error message to display.
    """
    messagebox.showerror("Error", "An error occured: " + msg)

def clear_window(win: "ctk.CTk") -> None:
    """
    Clears all stuff inside a window
    """
    for widget in win.winfo_children():
        widget.destroy()
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
    
def action_bar(win: "ctk.CTk", buttons: "tuple[tuple[str, callable], ...]") -> "tuple[ctk.CTkFrame, dict[str, ctk.CTkButton]]":
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

def quit() -> None:
    """
    Asks if the user wants to quit the application.
    """
    result = messagebox.askquestion("Confirm Action", "Are you sure you want to quit?")
    if result == "yes":
        f.dbg("GUI: Quitting application...")
        ctk.CTk().destroy()  # Close the main window
        f.quit(0)  # Call the quit function from function module
        
def not_implemented_yet() -> None:
    messagebox.showinfo("Not Implemented Yet", "This feature is not implemented yet.")
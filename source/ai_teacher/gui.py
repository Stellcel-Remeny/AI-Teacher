#
# This file deals with anything simple GUI related
# Copyright (c) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher import function as f
import customtkinter as ct
from tkinter import messagebox

def init(title: str = "Remeny AI Teacher", width: int = 800, height: int = 600) -> "ct.CTk":
    """
    Initialize a window
    """
    ct.set_appearance_mode("system")
    win = ct.CTk()
    win.geometry(f"{width}x{height}")
    win.iconbitmap("resources/icon.ico")
    win.resizable(True, True)
    return reinit(win, title)

def reinit(win: "ct.CTk", title: str = "Remeny AI Teacher") -> "ct.CTk":
    """
    Reinitialize a window
    """
    clear_window(win)
    win.title(title)
    f.dbg(f"Window is customized: title = '{title}'")
    return win

def error(msg: str) -> None:
    """
    Display an error message in a pop-up window.
    
    Args:
        msg (str): The error message to display.
    """
    messagebox.showerror("Error", "An error occured: " + msg)

def clear_window(win: "ct.CTk") -> None:
    """
    Clears all stuff inside a window
    """
    for widget in win.winfo_children():
        widget.destroy()
    f.dbg("Cleared window")
    
def banner(win: "ct.CTk", heading: str, text: str, height: int = 65) -> None:
    """
    Adds some user-friendly text at the top, expanding horizontally with window resize.
    """
    win.grid_columnconfigure(0, weight=1)

    frame = ct.CTkFrame(master=win, height=height)
    frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    frame.pack_propagate(False)  # Prevent content from shrinking the frame

    label_heading = ct.CTkLabel(
        master=frame,
        text=heading,
        font=ct.CTkFont(size=20, weight="bold"),
        justify="left"
    )
    label_heading.pack(anchor="w", padx=14, pady=(10, 0))  # Top padding only

    label_text = ct.CTkLabel(
        master=frame,
        text=text,
        font=ct.CTkFont(size=14),
        justify="left"
    )
    label_text.pack(anchor="w", padx=16, pady=(0, 5))  # Bottom padding only

    f.dbg(f"Added banner with heading: '{heading}' and text: '{text}'")

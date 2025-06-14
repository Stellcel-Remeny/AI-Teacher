#
# This file deals with anything simple GUI related
# Copyright (c) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher import function as f
import customtkinter as ctk
from tkinter import messagebox

def init(title: str = "Remeny AI Teacher", width: int = 800, height: int = 600) -> "ctk.CTk":
    """
    Initialize a window
    """
    ctk.set_appearance_mode("system")
    win = ctk.CTk()
    win.geometry(f"{width}x{height}")
    win.iconbitmap("resources/icon.ico")
    win.resizable(True, True)
    return reinit(win, title)

def reinit(win: "ctk.CTk", title: str = "Remeny AI Teacher") -> "ctk.CTk":
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

def clear_window(win: "ctk.CTk") -> None:
    """
    Clears all stuff inside a window
    """
    for widget in win.winfo_children():
        widget.destroy()
    f.dbg("Cleared window")
    
def banner(win: "ctk.CTk", heading: str, text: str, height: int = 65) -> None:
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

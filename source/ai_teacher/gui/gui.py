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

import customtkinter as ctk # type: ignore
import os
import platform

# ---[ Initialization ]--- #

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

# ---[ Primary functions ]--- #

def error(msg: str, title: str = "Error") -> None:
    """
    Display an error message in a pop-up window.
    
    Args:
        msg (str): The error message to display.
        title (str = "Error"): Window title
    """
    messagebox.showerror(title, f"An error occured: {msg}") # type: ignore
    
def warn(msg: str, title: str = "Warning!") -> None:
    """
    Display a warning
    
    Args:
        msg (str): The error message to display.
        title (str = "Error"): Window title
    """
    messagebox.showwarning(title, f"Warning: {msg}") # type: ignore
    
def quit() -> None:
    """
    Asks if the user wants to quit the application.
    """
    result = messagebox.askquestion("Confirm Action", "Are you sure you want to quit?") # type: ignore
    if result == "yes":
        f.dbg("GUI: Quitting application...")
        try:
            shared.root_app.destroy() # type: ignore
        except Exception as e:
            f.dbg(f"Exception during quit: {e}")
        f.quit(0)
    
# ---[ Secondary functions ]--- #

def not_implemented() -> None:
    messagebox.showinfo("Not Implemented Yet", "This feature is not implemented yet.") # type: ignore

def clear_window(win: "ctk.CTk") -> None:
    """
    Clears all stuff inside a window
    """
    for widget in win.winfo_children():
        widget.quit()
    f.dbg(f"Cleared window {win.winfo_name()}")
    
def clear_frame(frame: ctk.CTkFrame) -> None:
    """
    Clears all widgets inside the given frame.
    """
    for widget in frame.winfo_children(): # type: ignore
        widget.destroy() # type: ignore
    f.dbg(f"Cleared frame {frame.winfo_name()}")
    
# ---[ Window classes ]--- #

class app:
    """
    Application class for Remeny AI Teacher GUI.
    """
    def __init__(self, title: str = "Remeny AI Teacher", width: int = 800, height: int = 600):
        # Theme settings
        theme: str = shared.user_config.get('Main', 'theme', fallback="system").lower()
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
            self.root.iconbitmap(f"{shared.app_dir}/media/icons/icon.ico") # type: ignore
        else:
            xbm_path = f"{shared.app_dir}/media/icons/icon-0.xbm"
            if os.path.exists(xbm_path):
                self.root.iconbitmap(f"@{xbm_path}") # type: ignore
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
        self.main.grid(row=0, column=0, sticky="nsew") # type: ignore
        self.main.pack_propagate(False)  # Prevent content from shrinking the frame
        
        # Banner and action bar
        self.banner_frame = Banner(self.main, "Placeholder", "Edit these text using '.banner()'")
        f.dbg(f"Initialized new app with title: '{title}'")
    
    def banner(self, heading: str = "", text: str = "") -> None:
        """
        Edits the banner text and subtext the main window.
        
        Args:
            heading (str): The heading text for the banner.
            text (str): The subtext for the banner.
        """
        self.banner_frame.label_heading.configure(text=heading)
        self.banner_frame.label_text.configure(text=text)
        f.dbg(f"Updated banner with heading: '{heading}' and text: '{text}'")
        
    def action_bar(self, buttons: tuple[tuple[str, Callable[[], None]], ...]) -> None:
        """
        Adds/Re-adds an action bar with buttons to the main window.
        
        Args:
            buttons (tuple[tuple[str, Callable[[], None]], ...]): A tuple of button text and command pairs.
        """
        if hasattr(self, "action_bar_frame") and self.action_bar_frame:
            self.action_bar_frame.grid_forget()  # Remove the old action bar if it exists
            self.action_bar_frame.destroy()  # Destroy the old action bar frame if it exists
        
        self.action_bar_frame = ActionBar(self.root, buttons)
        self.buttons = self.action_bar_frame.button_refs
    
class Banner:
    def __init__(self, win: Union["ctk.CTkFrame", "ctk.CTkScrollableFrame"], heading: str, text: str, height: int = 65):
        """
        A banner widget that displays a heading and a subtext, horizontally stretchable.
        """
        win.grid_columnconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(master=win, height=height)
        self.frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")  # type: ignore
        self.frame.pack_propagate(False)

        self.label_heading = ctk.CTkLabel(
            master=self.frame,
            text=heading,
            font=ctk.CTkFont(size=20, weight="bold"),
            justify="left"
        )
        self.label_heading.pack(anchor="w", padx=14, pady=(10, 0))  # type: ignore

        self.label_text = ctk.CTkLabel(
            master=self.frame,
            text=text,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        self.label_text.pack(anchor="w", padx=16, pady=(0, 5))  # type: ignore

        f.dbg(f"Banner heading: '{heading}', text: '{text}'")
    
class ActionBar:
    def __init__(
        self,
        win: Union[ctk.CTk, ctk.CTkScrollableFrame, ctk.CTkFrame, ctk.CTkToplevel],
        buttons: tuple[tuple[str, Callable[[], None]], ...]
    ) -> None:
        """
        Adds a horizontal action bar with buttons at the bottom of the given window.
        """
        self.win = win
        self.buttons = buttons
        self.frame = self._create_action_frame()
            
        # Add version text
        version_text = ctk.CTkLabel(
            master=self.frame,
            text="Remeny AI Teacher v" + shared.version + " ",
            font=ctk.CTkFont(slant="italic"),
            justify="left"
        )
        version_text.pack(side="left", padx=9)
        
        # Add buttons to the action bar
        self.button_refs: dict[str, ctk.CTkButton] = {}
        self._add_buttons()

    def _create_action_frame(self) -> ctk.CTkFrame:
        self.win.rowconfigure(0, weight=1)
        self.win.rowconfigure(1, weight=0)
        self.win.columnconfigure(0, weight=1)

        action_frame = ctk.CTkFrame(master=self.win, height=40, corner_radius=10)
        action_frame.grid(row=1, column=0, sticky="ew")  # type: ignore
        action_frame.grid_propagate(False)
        return action_frame

    def _add_buttons(self) -> None:
        for text, command in self.buttons:
            button = ctk.CTkButton(master=self.frame, text=text, command=command)
            button.pack(side="right", padx=(5, 5), pady=5)  # type: ignore
            self.button_refs[text] = button

        f.dbg(f"Added action bar with buttons: {self.buttons}")

class CTkLabelledComboBox(ctk.CTkFrame):
    def __init__(
        self,
        master: Union[ctk.CTkFrame, ctk.CTkScrollableFrame],
        text: str,
        values: list[str],
        default_value: str = "",
        width: int = 200,
        height: int = 30,   
        *args, **kwargs # type: ignore
    ):
        super().__init__(master=master, width=width, height=height, *args, **kwargs) # type: ignore
        self.label = ctk.CTkLabel(self, text=text)
        self.label.pack(side="left", padx=5, pady=5) # type: ignore

        self.combobox = ctk.CTkComboBox(self, values=values, width=width - 50)
        self.combobox.pack(side="left", padx=5, pady=5) # type: ignore
        self.combobox.set(default_value)

    def get(self) -> str:
        return self.combobox.get()

    def set(self, value: str):
        self.combobox.set(value)
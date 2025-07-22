#
# This file shows login prompt
# Issue: User list can go beyond window size if too much users are present
#

# ---[ Libraries ]--- #
from ai_teacher.resources import shared
from ai_teacher.resources import functions as f
from ai_teacher.gui import gui

import tkinter as tk
import customtkinter as ctk # type: ignore
import os

# ---[ Global variables ]--- #
user_names: list[str] = []
user_directories: list[str] = f.list_dirs(os.path.join(shared.app_dir, "data"))

# ---[ Login windows ]--- #
def create_user(enable_back_button: bool = False) -> bool | None:
    """
    This function creates a new user account.
    It opens a new window where the user can enter a username.
    If the username is valid, it adds the user to the list of users.
    Returns True if the user was created successfully, False if the user creation was cancelled.
    """
    global return_value
    return_value = None
    f.dbg("Launching user creation wizard")
    def on_back() -> None:
        """
        Callback for the 'Go back' button.
        Closes the user creation window and returns to the login window.
        """
        global return_value
        f.dbg("Closing user creation window & returning to login window")
        return_value = False
        window.quit()
    
    def on_create_user() -> None:
        global user_names, return_value
        new_user_name = Entry_id1.get().strip()
        if not new_user_name:
            gui.warn("Username cannot be empty.")
        elif new_user_name in user_names:
            gui.warn(f"User '{new_user_name}' already exists. Please choose a different username.")
        elif len(new_user_name) < 3:
            gui.warn("Username must be at least 3 characters long.")
        elif len(new_user_name) > 20:
            gui.warn("Username must be at most 20 characters long.")
        elif not all(c.isalnum() or c.isspace() for c in new_user_name):
            gui.warn("Username can only contain alphanumeric and space characters.")
        elif new_user_name.replace(" ", "_").lower() in [name.lower() for name in user_directories]:
            gui.warn(f"User directory '{new_user_name.replace(' ', '_').lower()}' already exists. Please choose a different username.")
        else:
            f.dbg(f"Appending new user: {new_user_name}")
            user_names.append(new_user_name)
            f.dbg(f"Appending user directory...")
            user_directories.append(new_user_name.replace(" ", "_").lower())
            f.dbg("Closing user creation window")
            return_value = True
            window.quit()
    
    window = tk.Toplevel(shared.root_app)
    window.title("Create user")
    window.geometry("350x165")
    window.configure(bg="#FFFFFF")
    window.resizable(False, False)
    window.protocol("WM_DELETE_WINDOW", gui.quit)

    Button_id7 = ctk.CTkButton(
        master=window,
        text="Go back",
        font=("undefined", 14),
        text_color="#000000",
        hover=True,
        hover_color="#949494",
        height=30,
        width=95,
        border_width=2,
        corner_radius=6,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        command=on_back
        )
    Button_id7.place(x=5, y=120) # type: ignore
    Button_id6 = ctk.CTkButton(
        master=window,
        text="Quit APP",
        font=("undefined", 14),
        text_color="#000000",
        hover=True,
        hover_color="#949494",
        height=30,
        width=95,
        border_width=2,
        corner_radius=6,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        command=gui.quit
        )
    Button_id6.place(x=230, y=120) # type: ignore
    Button_id5 = ctk.CTkButton(
        master=window,
        text="Create",
        font=("undefined", 14),
        text_color="#000000",
        hover=True,
        hover_color="#949494",
        height=30,
        width=95,
        border_width=2,
        corner_radius=6,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        command=on_create_user
        )
    Button_id5.place(x=130, y=120) # type: ignore
    Label_id2 = ctk.CTkLabel(
        master=window,
        text="Enter username for new account:",
        font=("Arial", 14),
        text_color="#000000",
        height=30,
        width=224,
        corner_radius=0,
        bg_color="#FFFFFF",
        fg_color="#FFFFFF",
        )
    Label_id2.place(x=70, y=30) # type: ignore
    Entry_id1 = ctk.CTkEntry(
        master=window,
        placeholder_text="Username",
        placeholder_text_color="#454545",
        font=("Arial", 14),
        text_color="#000000",
        height=30,
        width=230,
        border_width=2,
        corner_radius=6,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        )
    Entry_id1.place(x=60, y=60) # type: ignore
    Label_id3 = ctk.CTkLabel(
        master=window,
        text="This account won't be saved until you log in once.",
        font=("Arial", 14),
        text_color="#000000",
        height=30,
        width=224,
        corner_radius=0,
        bg_color="#FFFFFF",
        fg_color="#FFFFFF",
        )
    Label_id3.place(x=20, y=90) # type: ignore

    # Check if we want to enable the back button
    if not enable_back_button:
        Button_id7.place_forget()

    #run the main loop
    window.mainloop()
    #Exit
    window.destroy()
    f.dbg(f"User creation window Return Val: {return_value}")
    return return_value

def refresh_user_list(radio_frame: ctk.CTkFrame, selected_user_var: tk.StringVar) -> None:
    global user_names, user_directories
    f.dbg("Refreshing user list")
    f.dbg(f"User names: {user_names}")
    f.dbg(f"User directories: {user_directories}")
    gui.create_list_radio_buttons(radio_frame, selected_user_var, user_names)
    
def display_login_prompt() -> str:
    """
    Displays a login prompt for the user to select or create a user.
    Returns the selected username and directory.
    """
    global selected_user, user_names, user_directories
    selected_user = ""
    def on_new() -> None:
        """
        Callback for the 'New' button.
        Opens a new user creation login_window.
        """
        login_window.withdraw()
        f.dbg("Login window hidden")
        
        if create_user(enable_back_button=True):
            f.dbg("User created successfully, refreshing user list")
            refresh_user_list(radio_frame, selected_user_var)
        
        login_window.deiconify()
        f.dbg("Login window shown")
            
    def on_login() -> None:
        """
        Callback for the 'Login' button.
        Validates the selected user and closes the login_window.
        """
        global selected_user
        selected_user = selected_user_var.get()
        if not selected_user:
            gui.warn("Please select a user before logging in.")
        else:
            f.dbg(f"User selected: {selected_user}")
            login_window.quit()
    
    login_window = tk.Toplevel(shared.root_app)
    login_window.title("Login")
    login_window.geometry("500x320")
    login_window.configure(bg="#FFFFFF")

    Button_id7 = ctk.CTkButton(
        master=login_window,
        text="New~",
        font=("undefined", 14),
        text_color="#000000",
        hover=True,
        hover_color="#949494",
        height=30,
        width=95,
        border_width=2,
        corner_radius=18,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        command=on_new
        )
    Button_id7.place(x=380, y=20) # type: ignore
    Button_id6 = ctk.CTkButton(
        master=login_window,
        text="Cancel",
        font=("undefined", 14),
        text_color="#000000",
        hover=True,
        hover_color="#949494",
        height=30,
        width=95,
        border_width=2,
        corner_radius=18,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        command=gui.quit
        )
    Button_id6.place(x=390, y=280) # type: ignore
    Button_id5 = ctk.CTkButton(
        master=login_window,
        text="Login",
        font=("undefined", 14),
        text_color="#000000",
        hover=True,
        hover_color="#949494",
        height=30,
        width=95,
        border_width=2,
        corner_radius=18,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        command=on_login
        )
    Button_id5.place(x=280, y=280) # type: ignore
    Label_id2 = ctk.CTkLabel(
        master=login_window,
        text="Select your account",
        font=("MS Gothic", 22),
        text_color="#000000",
        height=37,
        width=224,
        corner_radius=1,
        bg_color="#FFFFFF",
        fg_color="#FFFFFF",
        )
    Label_id2.place(x=20, y=10) # type: ignore

    # Frame to hold radio buttons
    radio_frame = ctk.CTkFrame(master=login_window, fg_color="#FFFFFF", width=300, height=200)
    radio_frame.place(x=20, y=60) # type: ignore

    # List users
    selected_user_var = tk.StringVar()
    refresh_user_list(radio_frame, selected_user_var)
    
    # run the main loop
    login_window.mainloop()
    
    # Exit the login window
    login_window.destroy()
    
    # Return the selected user
    return selected_user

def login_prompt() -> tuple[str, str]:
    """
    Prompts the user to login or create a new user.
    Returns the username.
    """
    global user_names, user_directories
    from configparser import ConfigParser
    # Gather user directories and names
    
    if not user_directories:
        # No users found, create a new user
        create_user()
    else:
        # Users are already present, populate user names
        current_config = ConfigParser()
        
        for directory in user_directories:
            settings_file = os.path.join(shared.app_dir, "data", directory, "settings.ini")
            
            if os.path.isfile(settings_file):
                f.dbg(f"Reading settings from {settings_file}")
                current_config.read(settings_file)
                user_name = current_config.get("Account", "pretty_name", fallback=f"NOOBUSER_<{directory}>")
            else:
                f.dbg(f"Settings file not found for {directory}.")
                user_name = f"NOOBUSER_<{directory}>"
            
            user_names.append(user_name)

    # Display a login window
    selected_user_name: str = ""
    selected_user_name = display_login_prompt()
    
    if not selected_user_name:
        f.quit(1, "Apparently selected_user_name is empty, how can I log in?")
    
    # Match the selected user name with our index
    index: int = 0
    f.dbg(f"Selected user name: {selected_user_name}")
    f.dbg(f"User names: {user_names}")
    try:
        index = user_names.index(selected_user_name)
    except ValueError:
        f.quit(1, f"User '{selected_user_name}' not found in user list!")

    return selected_user_name, user_directories[index]

def ask_session(win: gui.app) -> str:
    """
    Opens a simple GUI dialog asking the user to select a session type.
    Requires parent window.

    Returns:
        str: The user-selected session type as a string.
    """
    session_types: dict = {
        "basic": "Basic AI Text CHAT",
        "live_text_only" : "Live text chat (like WhatsApp) - Short messages",
        "live_speech": "Live text + speech & voice recognition",
        "video_no_camera": "Video chat without camera",
        "video_with_camera": "Video chat with camera"
    }
    display_names: list = list(session_types.values())
    selected_option: ctk.StringVar = ctk.StringVar()
    session_type_to_return: str = ""
    
    def on_next():
        nonlocal session_type_to_return
        selected_option_text = selected_option.get()
        session_type = next((k for k, v in session_types.items() if v == selected_option_text), None)
        
        if session_type is None:
            raise ValueError("Invalid session type selected (not found in dictionary).")
        
        # Convert to list for index
        session_keys = list(session_types.keys())
        index = session_keys.index(session_type) 
        
        if 0 < index < 5:
            gui.not_implemented()
        else:
            session_type_to_return = session_type
            gui.common_next()
    
    win.root.title("Remeny AI Teacher - Session Type")
    win.banner(f"Welcome, {shared.user_name}", "Select a session type to use the AI Teacher.")
    win.action_bar(buttons=(("Cancel", gui.quit), ("Next", on_next)))
    win.buttons["Next"].configure(state="disabled")

    # Frame to hold radio buttons
    radio_frame = ctk.CTkFrame(master=win.main, fg_color="#FFFFFF", width=300, height=200)
    radio_frame.grid(padx=60, pady=60)
    
    def on_session_button_select():
        win.buttons['Next'].configure(state="normal")
        return

    # List users
    gui.create_list_radio_buttons(radio_frame, selected_option, display_names, on_select=on_session_button_select)

    #run the main loop
    win.main.mainloop()
    
    if not session_type_to_return or session_type_to_return not in session_types:
        raise ValueError("Invalid session type. Something went wrong terribly. Quitting.")
    else:
        return session_type_to_return
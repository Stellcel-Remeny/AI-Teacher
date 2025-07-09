#
# Functions file for AI Teacher
# Copyright (C) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher.resources import shared

import os
import sys
import configparser
import time
import platform

from datetime import datetime

# ---[ Variables ]--- #
logfile_name: str
logfile_directory: str

# ---[ Primary Functions ]--- #
def log(text: str) -> str:
    """
    This function logs text to a file and returns
    a formatted string with added time
    """
    import re
    # Add time information
    text = f"\033[34m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m {text}"
    # Add log without color codes if enabled
    if shared.config.getboolean('Debug', 'enable_logging', fallback=False):
        global logfile_name, logfile_directory
        clean_text = re.sub(r'\x1B\[[0-9;]*m', '', text)
        os.makedirs(logfile_directory, exist_ok=True)
        with open(logfile_name, "a", encoding="utf-8") as f:
            f.write(f"{clean_text}\n")
    
    return text
    
def dbg(*args) -> None:
    """
    This function outputs text given to it to terminal,
    if debugging is enabled.
    """
    if not shared.debug:
        return
    
    text = " ".join(str(arg) for arg in args)
    formatted_text: str = f"\033[31m[Debug]\033[32m {text} \033[0m"
    print(log(formatted_text))
    
def quit(return_code: int, text: str = "", dialog: bool = True) -> None:
    """
    This function quits the program with a given return code.
    """
    # Quit root_app if it exists and quick_exit is true
    # Why? Sometimes if an error is shown, the background GUI will
    # still function. So if this option is enabled, we will close the GUI
    if shared.config.getboolean('GUI', 'quick_exit', fallback=True):
        try:
            if shared.root_app and shared.root_app.winfo_exists():
                try:
                    shared.root_app.destroy()
                except Exception as e:
                    dbg(f"Error destroying root_app: {e}")
                    return_code = 1
        except Exception:
            pass  # window already destroyed
    
    # Display error dialog if return_code != 0:
    if return_code != 0 and dialog:
        dbg(f"ERROR! RETURN CODE: {return_code}")
        dbg(f"Error message: {text}")
        print(f"An error occurred: {text}")
        gui.error(f"{text}\nReturn code: {return_code}")

    # Print exit message
    dbg(f"Quitting with return code {return_code}")
    print("Exiting...")
    
    # Print session information
    dbg(f"Session {shared.build_number} lasted from {shared.init_time_formatted} to {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    dbg("Program exited after running for {:.1f} seconds".format(time.time() - shared.init_time))
    exit(return_code)

# ---[ Secondary Functions ]--- #
def clear_screen():
    """
    This function clears the terminal
    """
    if not shared.config.getboolean('Debug', 'clear_terminal_on_startup', fallback=True):
        return
    
    dbg("Clearing screen...")
    
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    
def load_config(ini_file: str) -> configparser.ConfigParser:
    """
    This function loads given .ini file
    """
    config = configparser.ConfigParser()

    # Try to read the config file
    if not os.path.isfile(ini_file):
        print(f"Unable to load ini configuration file: {ini_file}")
        quit(1, "Unable to load configuration file.")

    config.read(ini_file)
    return config

def update_ini(ini_file: str, section: str, key: str, value: str) -> None:
    from configupdater import ConfigUpdater
    
    updater: ConfigUpdater = ConfigUpdater()
    dbg(f"Updating ini file '{ini_file}' with value '{value}' for section '{section}' and key '{key}'")
    updater.read(ini_file) # type: ignore

    if not updater.has_section(section): # type: ignore
        updater.add_section(str(section))

    updater[section][key] = value
    updater.update_file()
    
def update_config(section: str, key: str, value: str) -> None:
    """
    This function updates the main 'configuration.ini' file
    stored in shared.config_file as well as the configuration
    loaded in shared.config
    """
    update_ini(shared.config_file, section, key, value)
    
    # Update in-memory config
    if not shared.config.has_section(section):
        shared.config.add_section(str(section))
    
    shared.config[section][key] = str(value)
    return
    
def update_user_config(section: str, key: str, value: str) -> None:
    """
    This function updates the user's configuration ini file
    stored in shared.user_config_file as well as the user 
    configuration loaded in shared.user_config
    """
    update_ini(shared.user_config_file, section, key, value)
    
    # Update in-memory config
    if not shared.user_config.has_section(section):
        shared.user_config.add_section(str(section))
    
    shared.user_config[section][key] = str(value)
    return

def display_version() -> None:
    shared.build_number = str(int(shared.config.get('Version', 'build', fallback='0')) + 1)
    shared.version = (
        f"{shared.config.get('Version', 'major', fallback='0')}."
        f"{shared.config.get('Version', 'minor', fallback='0')}."
        f"{shared.config.get('Version', 'carry', fallback='0')}."
        f"{shared.build_number}"
    )
    print("\nRemeny AI Teacher")
    print(f"Version {shared.version}\n")
    # Update build number
    update_config('Version', 'build', shared.build_number)

def yesno(message: str) -> bool:
    """
    Displays a yes or no question in terminal
    """
    while True:
        answer = input(f"{message} [Y/N]: ").strip().lower()
        if answer == 'y':
            return True
        elif answer == 'n':
            return False

def create_folders() -> None:
    """
    Creates required folders
    """
    dbg("Making folders...")
    # Read the folder names from settings/folders.txt
    with open(f'{shared.app_dir}/settings/folders.txt', 'r', encoding='utf-8') as file:
        folder_names = [
            os.path.join(shared.app_dir, line.strip())
            for line in file if line.strip()
        ]

    # Create each folder
    for folder in folder_names:
        try:
            os.makedirs(folder, exist_ok=True)  # exist_ok=True avoids error if folder exists
        except Exception as e:
            print(f"Failed to create directory '{folder}': {e}")
            quit(1)
            
def list_dirs(path: str) -> list[str]:
    """
    Lists directories in the given path
    """
    try:
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    except FileNotFoundError:
        dbg(f"Directory not found: {path}")
        return []
    except Exception as e:
        dbg(f"Error listing directories in {path}: {e}")
        return []

# ---[ Init function ]--- #
def init() -> None:
    """
    Initialize our program
    """
    global logfile_name, logfile_directory
    # Variable initialization
    shared.init_time = time.time()
    shared.init_time_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    shared.app_dir = os.path.dirname(os.path.abspath(str(getattr(sys.modules['__main__'], '__file__', ''))))
    shared.config_file = os.path.join(shared.app_dir, "settings", "configuration.ini")
    shared.config = load_config(shared.config_file)
    shared.debug = shared.config.getboolean('Debug', 'enable_debug', fallback=False)
    shared.log = shared.config.getboolean('Debug', 'enable_logging', fallback=False)
    
    if shared.log:
        logfile_directory = os.path.join(shared.app_dir, shared.config.get('Debug', 'log_directory', fallback='logfiles'))
        logfile_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
        logfile_name = os.path.join(logfile_directory, logfile_name)
    
    # Libraries (put here so shared variables are accessible)
    from ai_teacher.gui import gui
    from ai_teacher.resources.notices import show_notices
    from ai_teacher.resources import sounds
    from ai_teacher.backend.login import login
    
    clear_screen()
    display_version()
    
    try:
        sounds.init()
    except Exception as e:
        quit(1, e)
    
    create_folders()
    gui.init()
    
    if not login():
        quit(1, "Login failure.")
    
    show_notices(f"{shared.app_dir}/text/DISCLAIMER.txt", "GPLv3")
    dbg("Initialization complete.")
    return

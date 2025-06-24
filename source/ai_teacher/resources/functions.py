#
# Functions file for AI Teacher
# Copyright (C) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher.resources import shared
from ai_teacher.gui import gui

import os
import sys
import configparser
import time
from datetime import datetime
from configupdater import ConfigUpdater

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
    
def dbg(text: str) -> None:
    """
    This function outputs text given to it to terminal,
    if debugging is enabled.
    """
    if not shared.config.getboolean('Debug', 'enable_debug', fallback=False):
        return
    
    formatted_text: str = f"\033[31m[Debug]\033[32m {text} \033[0m"
    print(log(formatted_text))
    
def quit(return_code: int, text: str = "") -> None:
    # Display error dialog if return_code != 0:
    if return_code != 0:
        dbg(f"ERROR! RETURN CODE: {return_code}")
        print(f"An error occurred: {text}")
        gui.error(text)

    # Print exit message
    dbg(f"Quitting with return code {return_code}")
    print("Exiting...")
    
    # Print session information
    dbg(f"Session {shared.build_number} lasted from {shared.init_time_formatted} to {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    dbg("Program exited after running for {:.1f} seconds".format(time.time() - shared.init_time))
    exit(return_code)

# ---[ Secondary Functions ]--- #
def load_config(ini_file: str) -> configparser.ConfigParser:
    """
    This function loads given .ini file
    """
    config = configparser.ConfigParser()

    # Try to read the config file
    if not os.path.isfile(ini_file):
        print(f"Unable to load ini configuration file: {ini_file}")
        quit(1)

    config.read(ini_file)
    return config

from configupdater import ConfigUpdater

def update_ini(ini_file: str, section: str, key: str, value: str) -> None:
    updater = ConfigUpdater()
    updater.read(ini_file)

    if not updater.has_section(section):
        updater.add_section(section)

    if updater.has_option(section, key):
        updater[section][key].value = value
    else:
        updater[section].add_option(key, value)

    with open(ini_file, 'w', encoding='utf-8') as f:
        updater.write(f)

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
    update_ini(shared.config_file, 'Version', 'build', shared.build_number)

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
            
def show_notices(disclaimer_file: str, license_name: str) -> None:
    """
    Outputs disclaimer file, and also tells
    that the software is licensed under 'license'
    """
    # Show disclaimer
    if not shared.config.getboolean('Main', 'disclaimer_accepted', fallback=False):
        with open(disclaimer_file, "r", encoding="utf-8") as f:
            disclaimer_text = f.read()
            
        print(disclaimer_text)
        if not yesno("Do you accept this disclaimer?"):
            print("Closing due to user not accepting the disclaimer...")
            quit(1,"You must accept the disclaimer to continue.")
        
        update_ini(shared.config_file, 'Main', 'disclaimer_accepted', 'true')
            
    # Show license
    if not shared.config.getboolean('Main', 'license_accepted', fallback=False):
        print ("\n ---------------------- ")
        print(f"This program is licensed under the {license_name} license.")
        print("You can find the full license text in 'LICENSE.txt'.\n")
        
        if not yesno("Do you accept the license mentioned above?"):
            print("Closing due to user not accepting the license mentioned above...")
            quit(1, "You must accept the license to continue.")
        
        update_ini(shared.config_file, 'Main', 'license_accepted', 'true')
        
# ---[ User login ]--- #
def login() -> bool:
    shared.user_name = input("Enter username (will create if not exist):")
    shared.user_dir = f"{shared.app_dir}/data/{shared.user_name}".lower()
    os.makedirs(shared.user_dir, exist_ok=True)
    dbg(f"Logging in as {shared.user_name}")
    return True

# ---[ Init function ]--- #
def init() -> None:
    """
    Initialize our program
    """
    global logfile_name, logfile_directory
    # Variable initialization
    shared.init_time = time.time()
    shared.init_time_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    shared.app_dir = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
    shared.config_file = os.path.join(shared.app_dir, "settings", "configuration.ini")
    shared.config = load_config(shared.config_file)
    logfile_directory = f"{shared.app_dir}/{shared.config.get('Debug', 'log_directory', fallback='logfiles')}"
    logfile_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    logfile_name = f"{logfile_directory}/{logfile_name}"
    
    display_version()
    create_folders()
    show_notices(f"{shared.app_dir}/text/DISCLAIMER.txt", "GPLv3")
    if not login():
        quit(1, "Login failure.")
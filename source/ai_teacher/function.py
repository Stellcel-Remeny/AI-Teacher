#
# Functions & global file for AI Teacher
# Copyright (C) 2025 Remeny
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from .global_variables import *
from ai_teacher import gui # For GUI related functions
from dotenv import load_dotenv # For loading user configuration
from datetime import datetime
import os

# ---[ Logging ]--- #
if debug:
    import logging
    import os
    from datetime import datetime

    # Generate Log directory
    os.makedirs("logfiles", exist_ok=True)

    # Generate log filename using current datetime
    log_filename = datetime.now().strftime("logfiles/%Y-%m-%d_%H-%M-%S.log")

    # Color formatter for console
    class ColorFormatter(logging.Formatter):
        def format(self, record):
            record.asctime = f"\033[34m{self.formatTime(record, self.datefmt)}\033[0m"
            return f"[{record.asctime}] {record.getMessage()}"

    # Plain formatter for logfile
    file_formatter = logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")

    # Handlers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter(datefmt="%Y-%m-%d %H:%M:%S"))

    file_handler = logging.FileHandler(log_filename, "a")
    file_handler.setFormatter(file_formatter)

    # Configure logger
    logging.basicConfig(level=logging.INFO, handlers=[console_handler, file_handler])

# ---[ Definitions ]--- #

def info(*msg, plain: str = None) -> None:
    """
    Logs both color (to console) and plain (to logfile).
    """
    logger = logging.getLogger()
    message_colored = " ".join(str(m) for m in msg)
    message_plain = plain or message_colored

    # Create log record
    record = logging.LogRecord(
        name=logger.name,
        level=logging.INFO,
        pathname=__file__,
        lineno=0,
        msg=message_plain,
        args=(),
        exc_info=None,
    )

    # Send to file (handler 1)
    logger.handlers[1].handle(record)

    # Override message with colored one for console
    record.msg = message_colored
    logger.handlers[0].handle(record)

def dbg(*msg) -> None:
    if debug:
        plain = " ".join(str(m) for m in msg)
        color_msg = f"\033[31m[Debug]\033[32m {plain} \033[0m"
        info(color_msg, plain=f"[Debug] {plain}")

# Quit
def quit(return_code: int, text: str = "") -> None:
    # Get BuildNumber
    with open(BuildNumberFile, "r") as count_content:
        BuildNumber = int(count_content.read())

    # Display error dialog if return_code != 0:
    if return_code != 0:
        dbg("ERROR! RETURN CODE:", return_code)
        print(f"An error occurred: {text}")
        gui.error(text)

    # Print exit message
    dbg("Quitting with return code", return_code)
    print("Exiting...")
    
    # Print session information
    dbg("Session", BuildNumber, "lasted from", init_time_formatted, "to", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    dbg("Program exited after running for {:.1f} seconds".format(time.time() - init_time))
    exit(return_code)

# Cleares screen
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Initializes the program
def init() -> None:
    # Clear any previous output
    dbg("Clearing screen")
    clear_screen()
    dbg("Press CTRL-C at anytime to quit.\n")

    #  --( Update Version String )--  #
    BuildNumber = update_build_number(DefaultBuildNumber, BuildNumberFile)
    version = f"{MajorVersion}.{MinorVersion}.{AlphaRelease}.{BuildNumber}"

    #  --( Application Initialization )--  #
    # Display application information
    print("AI Teacher")
    print("Version:", str(version) + "-\"" + codename + "\"")
    print("You have currently ran this script", BuildNumber, "times.\n")

    # Make folders
    create_folders()

    # Create settings.env if it doesn't exist
    if not os.path.exists(user_settings_file):
        dbg("Creating user settings file:", user_settings_file)
        with open(user_settings_file, 'w') as f:
            f.write("# User settings for AI Teacher\n")

    # Load user settings into memory
    dbg("Loading user settings...")
    load_dotenv(user_settings_file)

    # Make them agree to stuff
    disclaimer(os.getenv("DISCLAIMER_ACCEPTED", "false").lower(), "resources/DISCLAIMER.txt")
    license(os.getenv("LICENSE_ACCEPTED", "false").lower())

# Updates build number
def update_build_number(BuildNumber_Local: int, BuildNumberFile_Local: str) -> int:
   # Try to increment integer (times this has been ran)
    try:
        dbg("Reading file '" + BuildNumberFile_Local + "'")
        # Open the count file
        with open(BuildNumberFile_Local, "r") as count_content:
            BuildNumber_Local = int(count_content.read())

        # Increment value
        BuildNumber_Local += 1

        # Save this new value to the text file
        dbg("Saving value '" + str(BuildNumber_Local) + "' to file '" + BuildNumberFile_Local + "'\n")
        with open(BuildNumberFile_Local, "w") as count_output:
            count_output.write(str(BuildNumber_Local))

    except (FileNotFoundError, ValueError):
        # Error occured, so create the file
        print("A non-terminating exception occured trying to read integer from file '" + BuildNumberFile_Local + "'")
        print("Creating file '" + BuildNumberFile_Local + "' with value '1'\n")
        with open(BuildNumberFile_Local, "w") as count_output:
            count_output.write("1")

        BuildNumber_Local = 1

    return BuildNumber_Local

# Function to set or update an environment variable in a .env file
#
# Example usage:
# update_value("USER_NAME", "King Orange")
def update_value(key = str, value = str) -> None:
    lines = []
    found = False
    # Read all lines and update the key if found
    with open(user_settings_file, 'r') as f:
        for line in f:
            if line.strip().startswith(f"{key}="):
                lines.append(f"{key}={value}\n")
                found = True
                dbg("Updated env: \"" + key + "\" with value: \"" + value + "\"")
            else:
                lines.append(line)
    # If key was not found, add it
    if not found:
        lines.append(f"{key}={value}\n")
        dbg("Added env: \"" + key + "\" with value: \"" + value + "\"")
    # Write back to the file
    with open(user_settings_file, 'w') as f:
        f.writelines(lines)

# Disclaimer and License Functions
def disclaimer(DISCLAIMER_ACCEPTED: str, DISCLAIMER_FILE: str = "DISCLAIMER.txt") -> None:
    # Check if license is already accepted
    if DISCLAIMER_ACCEPTED == "true":
        return
    
    with open(DISCLAIMER_FILE, "r", encoding="utf-8") as f:
        disclaimer_text = f.read()

    print(disclaimer_text)

    # Ask for agreement
    while True:
        answer = input("Do you agree with this disclaimer? [Y/N]: ").strip().lower()
        if answer == 'y':
            update_value("DISCLAIMER_ACCEPTED", "true")
            break
        elif answer == 'n':
            print("Closing due to user unagreement...")
            quit(1)

def license(LICENSE_ACCEPTED: str) -> None:
    # Check if license is already accepted
    if LICENSE_ACCEPTED == "true":
        return
    
    print ("\n ---------------------- ")
    print("This program is licensed under the GNU General Public License v3.0.")
    print("You can find the full license text in 'LICENSE.txt'.\n")
    
    # Ask for agreement
    while True:
        answer = input("Do you agree with this license? [Y/N]: ").strip().lower()
        if answer == 'y':
            update_value("LICENSE_ACCEPTED", "true")
            break
        elif answer == 'n':
            print("Closing due to user unagreement...")
            quit(1)

# Creates folders
def create_folders() -> None:
    dbg("Making folders...")
    # Read the folder names from resources/folders.txt
    with open('resources/folders.txt', 'r', encoding='utf-8') as file:
        folder_names = [line.strip() for line in file if line.strip()]

    # Create each folder
    for folder in folder_names:
        try:
            os.makedirs(folder, exist_ok=True)  # exist_ok=True avoids error if folder exists
        except Exception as e:
            print(f"Failed to create directory '{folder}': {e}")
            quit(1)
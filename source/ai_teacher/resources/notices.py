#
# This file shows disclaimer and license information
# as either a GUI window or a console output.
#

# ---[ Libraries ]--- #
from ai_teacher.resources import shared
from ai_teacher.resources import functions as f
from ai_teacher.gui import gui

import os

def show_notices_gui() -> "gui.app":
    """
    Creates a window to show the disclaimer and license information.
    """
    win = gui.app()
    win.root.title("Remeny AI Teacher")
    
    win.main = gui.Frame(win.root, "Notices", "Please read the following notices before proceeding.")
    
    return win

def show_disclaimer(disclaimer_file: str) -> None:
    """
    Shows the disclaimer to the user.
    """
    if not os.path.isfile(disclaimer_file):
        f.quit(1, f"Disclaimer file '{disclaimer_file}' not found. Please ensure it exists in the expected location.")
    
    with open(disclaimer_file, "r", encoding="utf-8") as file:
        disclaimer_text = file.read()
            
        print(disclaimer_text)
        if not f.yesno("Do you accept this disclaimer?"):
            print("Closing due to user not accepting the disclaimer...")
            f.quit(1,"You must accept the disclaimer to continue.")
        
        f.update_ini(shared.user_config_file, 'Main', 'disclaimer_accepted', 'true')

def show_license(license_name: str) -> None:
    # Show license
    if not shared.user_config.getboolean('Main', 'license_accepted', fallback=False):
        print ("\n ---------------------- ")
        print(f"This program is licensed under the {license_name} license.")
        print("You can find the full license text in 'LICENSE.txt'.\n")
        
        if not f.yesno("Do you accept the license mentioned above?"):
            print("Closing due to user not accepting the license mentioned above...")
            f.quit(1, "You must accept the license to continue.")
        
        f.update_ini(shared.user_config_file, 'Main', 'license_accepted', 'true')
        
def show_notices(disclaimer_file: str, license_name: str) -> None:
    if not shared.user_config.getboolean('Main', 'disclaimer_accepted', fallback=False):
        show_disclaimer(disclaimer_file)
        
    if not shared.user_config.getboolean('Main', 'license_accepted', fallback=False):
        show_license(license_name)
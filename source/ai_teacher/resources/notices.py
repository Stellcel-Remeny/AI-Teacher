#
# This file shows disclaimer and license information
# as either a GUI window (from gui.notices) or a console output.
#

# ---[ Libraries ]--- #
from ai_teacher.resources import shared
from ai_teacher.resources import functions as f
from ai_teacher.gui import gui
from ai_teacher.gui import notices as gui_notices

from typing import Union

import os

# ---[ Definitions ]--- #
def show_disclaimer(disclaimer_text: str) -> None:
    """
    Shows the disclaimer to the user via commandline.
    """
    print(disclaimer_text)
    if not f.yesno("Do you accept this disclaimer?"):
        print("Closing due to user not accepting the disclaimer...")
        f.quit(1,"You must accept the disclaimer to continue.")
        
    f.update_ini(shared.user_config_file, 'Main', 'disclaimer_accepted', 'true')

def show_license(license_text: str) -> None:
    """
    Shows the license to the user via commandline.
    """
    if not shared.user_config.getboolean('Main', 'license_accepted', fallback=False):
        print ("\n ---------------------- ")
        print(license_text)
        
        if not f.yesno("Do you accept the license mentioned above?"):
            print("Closing due to user not accepting the license mentioned above...")
            f.quit(1, "You must accept the license to continue.")
        
        f.update_ini(shared.user_config_file, 'Main', 'license_accepted', 'true')
        
def show_notices(disclaimer_file: str, license_name: str) -> None:
    """
    Shows the notices to the user, either via GUI or console.
    """
    use_gui: bool = shared.config.getboolean('GUI', 'notices', fallback=True)
    
    # Prepare variables
    if not os.path.isfile(disclaimer_file):
        f.quit(1, f"Disclaimer file '{disclaimer_file}' not found. Please ensure it exists in the expected location.")
    
    with open(disclaimer_file, "r", encoding="utf-8") as file:
        disclaimer_text: str = file.read()
    
    license_text: str = (
        f"This program is licensed under the {license_name} license.\n"
        "You can find the full license text in 'LICENSE.txt'.\n"
    )
    
    disclaimer_accepted: bool = shared.user_config.getboolean('Main', 'disclaimer_accepted', fallback=False)
    license_accepted: bool = shared.user_config.getboolean('Main', 'license_accepted', fallback=False)
    
    # Check if we should use GUI
    if use_gui and (not disclaimer_accepted or not license_accepted):
        gui_notices.show_notices_gui(disclaimer_text, disclaimer_accepted, license_text, license_accepted)
        return
    
    # The following are console-based notices
    if not disclaimer_accepted:
        show_disclaimer(disclaimer_text)
        
    if not license_accepted:
        show_license(license_text)
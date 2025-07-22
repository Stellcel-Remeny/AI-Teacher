#
# This file contains backend for User login
#

# ---[ Libraries ]--- #
from ai_teacher.resources import functions as f
from ai_teacher.resources import shared
from ai_teacher.gui import login as gui_login

import os

# ---[ Functions ]---- #
def login():
    #
    # This function logs in a user
    #
    # TODO: Add passwords
    #
    shared.user_name, shared.user_dir = gui_login.login_prompt()
    shared.user_dir = os.path.join(shared.app_dir, "data", shared.user_dir)
    f.dbg(f"The Chosen Username: {shared.user_name}")
    f.dbg(f"The Chosen User Directory: {shared.user_dir}")
    os.makedirs(shared.user_dir, exist_ok=True)
        
    shared.user_config_file = os.path.join(shared.user_dir, "settings.ini")
    
    if os.path.isfile(shared.user_config_file):
        f.dbg(f"Loading user configuration from pre-existing settings.ini file")
        shared.user_config = f.load_config(shared.user_config_file)
    else:
        default_config: str = os.path.join(shared.app_dir, "settings", "default.ini")
        f.dbg(f"Loading default user configuration from '{default_config}'")
        shared.user_config = f.load_config(default_config)
        f.dbg(f"Writing default values to user configuration")
        
        with open (shared.user_config_file, 'w', encoding='utf-8') as file:
            shared.user_config.write(file)
            
        f.dbg(f"Adding pretty name {shared.user_name}")
        f.update_user_config('Account', 'pretty_name', shared.user_name)
        f.dbg(f"Reloading to make sure changes are made")
        shared.user_config.clear()
        shared.user_config = f.load_config(shared.user_config_file)
    
    f.dbg(f"Logging in as {shared.user_name}")
    f.dbg(f"User directory full path at: {shared.user_dir}")
    return
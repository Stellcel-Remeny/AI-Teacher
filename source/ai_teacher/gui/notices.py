#
# This file shows notices in a GUI Window
#

# ---[ Libraries ]--- #
from ai_teacher.resources import shared
from ai_teacher.resources import functions as f
from ai_teacher.gui import gui

import customtkinter as ctk

def show_notices_gui(disclaimer_text: str,
                     disclaimer_accepted: bool,
                     license_text: str,
                     license_accepted: bool) -> None:
    """
    Creates a window to show the disclaimer and license information.
    """
    def on_action_next() -> None:
        """
        Action for the 'Next' button, which closes the window.
        """
        # Save the acceptance state
        f.update_ini(shared.user_config_file, 'Main', 'disclaimer_accepted', str(disclaimer_checkbox.get()).lower())
        f.update_ini(shared.user_config_file, 'Main', 'license_accepted', str(license_checkbox.get()).lower())
        
        win.root.quit()
        win.root.destroy()
    
    win = gui.app()
    win.root.title("Remeny AI Teacher")
    
    win.banner("Notices", "Please read the following before proceeding.")
    win.action_bar(buttons=(("Cancel", gui.quit), ("Next", on_action_next)))
    win.buttons["Next"].configure(state="disabled")
    
    # Common button check for license and disclaimer acceptance
    def on_button_check() -> None:
        """
        Enable the 'Next' button if both disclaimer and license are accepted.
        """
        if disclaimer_checkbox.get() and license_checkbox.get():
            win.buttons["Next"].configure(state="normal")
        else:
            win.buttons["Next"].configure(state="disabled")
    
    # Add our disclaimer text box and checkbox
    disclaimer_text_box = ctk.CTkTextbox(win.main, width=700, height=150, wrap="word")
    disclaimer_text_box.insert("1.0", disclaimer_text)
    disclaimer_text_box.configure(state="disabled") # Disable editing of the text box
    disclaimer_text_box.grid(row=1, padx=50, pady=20, sticky="ew")
    
    disclaimer_checkbox = ctk.CTkCheckBox(win.main, text="I accept the disclaimer", command=on_button_check)
    disclaimer_checkbox.grid(row=2, column=0, padx=50, pady=(0, 20), sticky="w")
    
    if disclaimer_accepted:
        disclaimer_checkbox.select()
    
    # Add our license text box and checkbox
    license_text_box = ctk.CTkTextbox(win.main, width=700, height=150, wrap="word")
    license_text_box.insert("1.0", license_text)
    license_text_box.configure(state="disabled")  # Disable editing of the text box
    license_text_box.grid(row=3, column=0, padx=50, pady=20, sticky="ew")
    
    license_checkbox = ctk.CTkCheckBox(win.main, text="I accept the license", command=on_button_check)
    license_checkbox.grid(row=4, column=0, padx=50, pady=(0, 20), sticky="w")
    
    if license_accepted:
        license_checkbox.select()
    
    # Mainloop
    win.root.mainloop()
    return
#
# Python camera GUI
# Copyright (C) 2025 Remeny
#

# ---[ Libraries ]--- #
from ai_teacher.resources import functions as f
from ai_teacher.resources import shared
from ai_teacher.backend import camera_backend
from ai_teacher.gui import gui

import customtkinter as ctk
import cv2
from PIL import Image, ImageTk

cam: "cv2.VideoCapture" = None  # Global variable to store the camera instance
cameras: list = []  # List to store available cameras
camera_names: list = []  # List to store camera names
previous_camera_index: int = None # To track the previously selected camera index in change_selected_camera
frame_update_id: int = None
user_instruction_index: int = 0
user_instruction_file: str
user_image_filename_stored_file: str
user_image_folder: str
user_image_names: list = []
user_instructions: list = []
init_shown: bool = False  # Flag to check if instructions have been shown

def init(win: "gui.mainapp") -> None:
    """
    Creates a window for selecting a camera to learn head positions.
    """
    # Variable initialization
    global user_instruction_file, user_image_filename_stored_file, user_image_folder
    user_instruction_file = f"{shared.app_dir}/text/camera/camera_user_instructions.txt"
    user_image_filename_stored_file = f"{shared.app_dir}/text/camera/head_position_filenames.txt"
    user_image_folder = f"{shared.user_dir}/trained_head_positions"
    
    global cameras, text_1, action_buttons
    win.root.title("Remeny AI Teacher - Camera Trainer")
    gui.banner(win.main, "Camera Trainer", "Select a camera to train the AI teacher.")
    action_bar, action_buttons = gui.action_bar(
        win.root,
        buttons=(("Next", gui.not_implemented), ("Cancel", gui.quit))
    )
    
    action_buttons["Next"].configure(state="disabled")
    
    cameras = camera_backend.list_cameras()
    if not cameras:
        # No cameras are available
        f.quit(1, "No cameras are available. Check if you have permissions, or connect a camera if you don't have one.")

    add_camera_selector(win.main)
    
    # Instruction text
    text_1 = ctk.CTkLabel(
        master=win.main,
        text="Loading...",
        font=ctk.CTkFont(size=14),
        justify="center"
    )
    text_1.grid(pady=(0, 5))  # Add some space below the text
    
    add_camera_preview(win.main)
    text_1.configure(text="Select a camera from the dropdown above to start.")
    add_capture_info(win.main)
    
    f.dbg("Waiting for camera selection...")
    
    win.root.mainloop()

def add_camera_selector(main: "ctk.CTkFrame") -> None:
    """
    Adds the first frame with camera selection options.
    Meant only to be executed once.
    """
    global frame1, frame2, combobox_1, cameras, camera_names
    # Container frame to hold label and combobox
    frame1 = ctk.CTkFrame(master=main, height=40, width=320)
    frame1.grid(padx=50, pady=20, sticky="w")  # Margin for the whole row
    # Prevent the frame from shrinking to fit its children
    frame1.grid_propagate(False)

    label_text = ctk.CTkLabel(
        master=frame1,
        text="Use camera:",
        font=ctk.CTkFont(size=14),
        justify="left"
    )
    label_text.grid(row=0, column=0, sticky="w", padx=(10, 10))  # Space between label and combo

    camera_names = [camera_num[1] for camera_num in cameras]

    combobox_1 = ctk.CTkComboBox(
        frame1,
        values=camera_names,
        width=210,
        command=lambda selected: change_selected_camera(frame2, camera_names.index(selected), selected)
    )
    combobox_1.set("")  # Set to empty string initially
    combobox_1.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=6)

def change_selected_camera(frame: "ctk.CTkFrame", camera_index: int, selected_camera: str, reload: bool = False) -> None:
    global cam, frame_update_id, button_1, button_2, previous_camera_index
    capture_image(init_text = True) # Update instruction text
    button_1.configure(state="normal")  # Enable the capture button
    button_2.configure(state="normal")  # Enable the reload button
    
    f.dbg(f"Selecting camera: {selected_camera} at index {camera_index}")
    
    if previous_camera_index == camera_index and not reload:
        f.dbg(f"Selected camera is same as previous one at index {camera_index}")
        return
    else:
        f.dbg("This select is a reload.")
    
    # Cancel previous frame update loop if it exists
    if frame_update_id is not None:
        frame.after_cancel(frame_update_id)
        f.dbg("Previous update loop canceled.")
        frame_update_id = None
    
    # Release the previous camera if it exists
    if cam is not None and cam is not False:
        f.dbg(f"Releasing camera: {cam}")
        cam.release()
    
    # Remove old widgets inside the frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    cam = camera_backend.init(camera_index)
    if cam is False:
        gui.error("Camera initialization failed. Please make sure you have access and that the camera is working.")
        return

    # Always recreate the label after clearing the frame
    frame.video_label = ctk.CTkLabel(frame, width=320, height=320, text="")
    frame.video_label.pack()
    frame.video_label.pack_propagate(False)

    def update_frame():
        global frame_update_id  # so we can cancel it later

        ret, img = cam.read()
        if not ret:
            f.dbg("Failed to grab frame from camera.")
            gui.error("Failed to grab frame from camera. Please check the camera connection.")
            return

        # Convert the image from BGR to RGB format
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)

        # Resize while maintaining aspect ratio to fit within 320x320
        img.thumbnail((320, 320), Image.LANCZOS)

        # Create a black canvas and paste the image centered
        canvas = Image.new("RGB", (320, 320), (0, 0, 0))
        offset_x = (320 - img.width) // 2
        offset_y = (320 - img.height) // 2
        canvas.paste(img, (offset_x, offset_y))

        img = ImageTk.PhotoImage(canvas)

        frame.video_label.configure(image=img)
        frame.video_label.image = img

        # Save ID to allow cancellation later
        frame_update_id = frame.after(60, update_frame)

    update_frame()
    previous_camera_index = camera_index
    
def add_camera_preview(frame: "ctk.CTkFrame") -> None:
    """
    Adds the second frame to display the camera feed.
    Meant only to be executed once.
    """
    global frame2
    # Container frame for camera display
    frame2 = ctk.CTkFrame(master=frame, height=320, width=320)
    frame2.grid(padx=50, pady=(0, 20))  # Margin for the whole row
    
def add_capture_info(frame: "ctk.CTkFrame") -> None:
    """
    Adds a button to capture the current frame and some text to tell the user what to do.
    Meant only to be executed once.
    """
    global button_1, button_2
    # Container to hold the two buttons side by side
    button_row = ctk.CTkFrame(master=frame, fg_color="transparent")
    button_row.grid(pady=(0, 20))  # Center this row in the main frame

    # Button 1 - Capture
    button_1 = ctk.CTkButton(
        master=button_row,
        text="Capture",
        state="disabled",
        command=lambda: capture_image()
    )
    button_1.grid(row=0, column=0, padx=10)  # Space between buttons

    # Button 2 - Reload
    button_2 = ctk.CTkButton(
        master=button_row,
        text="Reload camera",
        state="disabled",
        command=lambda: change_selected_camera(
            frame2,
            camera_names.index(combobox_1.get()),
            combobox_1.get(),
            reload=True
        )
    )
    button_2.grid(row=0, column=1, padx=10)

    f.dbg(f"Capture and Reload buttons added to frame: {frame}")
    
    text_2 = ctk.CTkLabel(
        master=frame,
        text="Press the 'Capture' button to capture the current frame.\n"
             "You can use this to train the AI teacher on your head positions.",
        font=ctk.CTkFont(size=14),
        justify="center"
    )
    text_2.grid(pady=(0, 20))  # Add some space below the text
    
def capture_image(init_text: bool = False) -> None:
    """
    Capture the current frame from the camera and save it.
    """
    global cam, init_shown, user_instruction_index, user_instructions, user_instruction_file, text_1, combobox_1, button_1, action_buttons
    
    if init_text:
        if not init_shown:
            get_instructions()
            f.dbg(f"Instruction messages: {user_instructions}")
            f.dbg(f"Head_position filenames: {user_image_names}")
            init_shown = True
        return
    
    if not camera_backend.write_image(cam, f"{shared.user_dir}/trained_head_positions/{user_image_names[user_instruction_index]}"):
        gui.error("Failed to capture image from camera.")
        return
    
    # Check so that it doesn't throw index out of range error next time
    if user_instruction_index + 1 < len(user_instructions):
        user_instruction_index += 1
        text_1.configure(text=user_instructions[user_instruction_index])
    else:
        f.dbg("No more instructions or next instruction is empty/null.")
        text_1.configure(text="Awesome. Click 'next' to continue.")
        button_1.configure(state="disabled")  # Disable the button after capturing is finished
        button_2.configure(state="disabled") # Disable the reload button
        combobox_1.configure(state="disabled") # Disable the combobox after capturing is finished
        action_buttons["Next"].configure(state="normal") # Enable the next button to continue
    
def get_instructions() -> None:
    global user_instruction_index, user_instructions, user_instruction_file
    global user_image_folder, user_image_filename_stored_file
    global user_image_names, text_1

    try:
        # Read user instructions
        with open(user_instruction_file, 'r') as f1:
            user_instructions = [line.strip() for line in f1]
        f.dbg(f"Finished reading user instructions from file: {user_instruction_file}")
        text_1.configure(text=user_instructions[user_instruction_index])
        user_instruction_index = 0

        # Read image filenames
        with open(user_image_filename_stored_file, 'r') as f2:
            user_image_names = [line.strip() for line in f2]
        f.dbg(f"Finished reading filenames from file '{user_image_filename_stored_file}'.")
        
            # Check if lengths match
        if len(user_instructions) != len(user_image_names):
            raise ValueError(
                f"Instruction count ({len(user_instructions)}) does not match filename count ({len(user_image_names)})."
            )

    except FileNotFoundError as e:
        f.quit(1, f"Error: File not found - {e.filename}")
    except PermissionError as e:
        f.quit(1, f"Error: No permission to read - {e.filename}")
    except IndexError:
        f.quit(1, f"Error: user_instruction_index is out of range: {user_instruction_index}")
    except ValueError as e:
        f.quit(1, f"Mismatch error: {e}")
    except Exception as e:
        f.quit(1, f"Unexpected error: {e}")
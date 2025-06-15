#
# Python camera GUI
# Copyright (C) 2025 Remeny
#

import customtkinter as ctk
from ai_teacher import optics
from ai_teacher import gui
from ai_teacher import function as f
import cv2
from PIL import Image, ImageTk

cam: "cv2.VideoCapture" = None  # Global variable to store the camera instance
cameras: list = []  # List to store available cameras
frame_update_id: int = None

def cam_init(win: "ctk.CTk") -> None:
    """
    Creates a window for selecting a camera to learn head positions.
    """
    global cameras
    content = gui.reinit(win, "Remeny AI Teacher - Camera Trainer")
    gui.banner(win, "Camera Trainer", "Select a camera to train the AI teacher.")
    
    cameras = optics.list_cameras()
    if not cameras:
        # No cameras are available
        f.quit(1, "No cameras are available. Check if you have permissions, or connect a camera if you don't have one.")

    add_camera_selector(win)
    
    # Instruction text
    text1 = ctk.CTkLabel(
        master=win,
        text="Loading...",
        font=ctk.CTkFont(size=14),
        justify="center"
    )
    text1.grid(pady=(0, 5))  # Add some space below the text
    
    add_camera_preview(win)
    add_capture_info(win)
    
    win.mainloop()

def change_selected_camera(frame: "ctk.CTkFrame", camera_index: int, selected_camera: str) -> None:
    global cam, frame_update_id # Use a global variable to store the camera instance
    
    f.dbg(f"Selecting camera: {selected_camera} at index {camera_index}")
    
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
    
    cam = optics.init(camera_index)
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
    
def add_camera_selector(win: "ctk.CTk") -> None:
    """
    Adds the first frame with camera selection options.
    Meant only to be executed once.
    """
    global frame1, frame2, combobox_1, cameras
    # Container frame to hold label and combobox
    frame1 = ctk.CTkFrame(master=win, height=40, width=320)
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
    combobox_1.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=6)
    
def add_camera_preview(win: "ctk.CTk") -> None:
    """
    Adds the second frame to display the camera feed.
    Meant only to be executed once.
    """
    global frame2
    # Container frame for camera display
    frame2 = ctk.CTkFrame(master=win, height=320, width=320)
    frame2.grid(padx=50, pady=(0, 20))  # Margin for the whole row
    
def add_capture_info(win: "ctk.CTk") -> None:
    """
    Adds a button to capture the current frame and some text to tell the user what to do.
    Meant only to be executed once.
    """
    global button1, text1
    button1 = ctk.CTkButton(
        master=win,
        text="Capture",
        command=lambda: f.dbg("Capture button pressed - implement capture logic here")
    )
    button1.grid(pady=(0, 20))  # Add some space below the button
    f.dbg("Capture button added to the window.")
    
    text2 = ctk.CTkLabel(
        master=win,
        text="Press the 'Capture' button to capture the current frame.\n"
             "You can use this to train the AI teacher on your head positions.",
        font=ctk.CTkFont(size=14),
        justify="center"
    )
    text2.grid(pady=(0, 20))  # Add some space below the text
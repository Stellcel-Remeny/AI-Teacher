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
frame_update_id: int = None

def init(win: "ctk.CTk") -> None:
    """
    Creates a window for selecting a camera to learn head positions.
    """
    gui.reinit(win, "Remeny AI Teacher - Camera Trainer")
    gui.banner(win, "Camera Trainer", "Select a camera to train the AI teacher.")
    
    cameras: list = optics.list_cameras()
    if not cameras:
        # No cameras are available
        f.quit(1, "No cameras are available. Check if you have permissions, or connect a camera if you don't have one.")

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
    
    # Container frame for camera display
    frame2 = ctk.CTkFrame(master=win, height=320, width=320)
    frame2.grid(padx=50, pady=(0, 20))  # Margin for the whole row
    
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

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
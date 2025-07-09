#
# NEW: Python face detection using Google MediaPipe
# For Remeny AI-Teacher
#

# ---[ Libraries ]--- #
from ai_teacher.resources import functions as f
from ai_teacher.resources import shared
from ai_teacher.resources.sounds import sounds
from ai_teacher.backend import camera as camera_backend
from ai_teacher.gui import gui

from PIL import Image, ImageTk # type: ignore
from typing import Union

import customtkinter as ctk # type: ignore
import cv2
import mediapipe as mp # type: ignore
import threading

# ---[ Variables ]--- #
cap = None
frame_loop_id = None
face_mesh = None
capture_countdown_id: str | None = None

# Store latest detected face points
latest_face_points = {
    "nose": None,
    "left_iris": None,
    "right_iris": None
}

def camera_trainer() -> None:
    """
    This function shows camera window.
    """
    instruction_updated: bool = False
    
    def on_combobox_selected(cam_name: str) -> None:
        capture_button.configure(text="Capture", state="normal") # type: ignore
        # Find camera index by name
        index = dict((name, idx) for idx, name in cameras).get(cam_name)
        if index is not None:
            open_face_track(image_label, index, debug_label=win.action_bar_frame.text)
            # Update instruction label
            nonlocal instruction_updated
            if not instruction_updated:
                instruction_label.configure(text=camera_backend.user_instructions[0])
                instruction_updated = True
                f.dbg(f"First instruction added: {camera_backend.user_instructions[0]}")
        else:
            f.quit(1, f"Selected camera '{cam_name}' not found.")
    
    # Basic window init
    win = shared.main_app
    win.root.title("Remeny AI Teacher - Camera Trainer")
    win.banner("Camera calibrator", "Select a camera and train the machine to know where you are looking.")
    win.action_bar(buttons=(("Cancel", gui.quit), ("Next", gui.common_next)))
    win.buttons["Next"].configure(state="disabled")
    
    # Populate the camera combobox
    cameras = camera_backend.list_cameras()
    if not cameras:
        f.quit(1, "No cameras are available. Check if you have permissions, or connect a camera if you don't have one.")
        
    camera_names = [name for (_, name) in cameras]
    
    combobox_cam_selector = gui.CTkLabelledComboBox(win.main, "Use camera:", camera_names)
    combobox_cam_selector.combobox.configure(command = on_combobox_selected) # type: ignore
    combobox_cam_selector.grid(padx=50, pady=20, sticky="w") # type: ignore
    
    # Instruction label (the one that displays on top of camera preview frame)
    instruction_label = ctk.CTkLabel(
        master=win.main,
        text="Loading...",
        font=ctk.CTkFont(size=14),
        justify="center"
    )
    instruction_label.grid(pady=(0, 5))
    
    # Camera preview frame
    image_frame = ctk.CTkFrame(win.main, width=500, height=500)
    image_frame.grid_propagate(False)
    image_frame.grid(pady=20)
    
    image_label = ctk.CTkLabel(image_frame, text="", font=("Verdana", 80))
    image_label.grid(row=0, column=0, sticky="nsew")
    image_frame.rowconfigure(0, weight=1)
    image_frame.columnconfigure(0, weight=1)
    
    def on_capture() -> None:
        global capture_countdown_id
        
        if capture_countdown_id is not None:
            capture_button.after_cancel(capture_countdown_id)
            capture_countdown_id = None
            capture_button.configure(text="Capture")
            image_label.configure(text="")
            f.dbg("Cancelled existing capture opteration.")
            return
            
        if None in latest_face_points.values():
            gui.warn("Face points not available yet.")
            return

        try:
            countdown_num = int(capture_delay_entry.get())
        except Exception:
            gui.warn("Invalid number input.")
            return

        # Start countdown
        def countdown(n: int):
            global capture_countdown_id
            if n <= 0:
                capture_button.configure(text="Capture")
                image_label.configure(text="")
                capture_countdown_id = None
                
                if None in latest_face_points.values():
                    gui.warn("Face points not found.")
                    return

                next_instruction: str = camera_backend.capture_face_points(
                    [left_x, left_y, left_z],
                    [right_x, right_y, right_z],
                    [nose_x, nose_y, nose_z]
                )
                
                # Update instruction label
                if next_instruction == "END":
                    # We reached end of instructions (hopefully)
                    instruction_label.configure(text="Awesome! You may continue by clicking 'Next'.")
                    capture_button.configure(state="disabled")
                    win.buttons['Next'].configure(state="normal")
                    f.dbg("Camera section seems to be finished.")
                else:
                    instruction_label.configure(text=next_instruction)
            else:
                f.dbg(f"Seconds remaining before capture: {n}")
                sounds["tick1"].play()
                image_label.configure(text=str(n))
                capture_button.configure(text=str(n))
                capture_countdown_id = capture_button.after(1000, countdown, n - 1)

        countdown(countdown_num)
        
    # Frame which holds capture button & delay input box
    control_frame = ctk.CTkFrame(win.main)
    control_frame.grid()
    
    capture_button = ctk.CTkButton(control_frame, text="Select a camera", command=on_capture, state="disabled")
    capture_button.grid(row=0, column=0, padx=10, pady=10)

    capture_delay_label = ctk.CTkLabel(control_frame, text="Delay:")
    capture_delay_label.grid(row=0, column=1)

    capture_delay_entry = gui.CTkNumberEntry(control_frame)
    capture_delay_entry.grid(row=0, column=2, padx=10, pady=10)
    
    instruction_label.configure(text="Please select a camera from above.\nAfter selecting, instructions will appear here. For capture button, scroll down.")
    
    win.main.mainloop()

def open_face_track(image_label: "ctk.CTkLabel",
                    camera_index: int,
                    debug_label: Union["ctk.CTkLabel", None] = None) -> None:
    global cap, frame_loop_id, face_mesh
    global nose_x, nose_y, nose_z, left_x, left_y, left_z, right_x, right_y, right_z

    if frame_loop_id:
        try: image_label.after_cancel(frame_loop_id)
        except: pass
        frame_loop_id = None

    if cap and cap.isOpened(): cap.release()
    f.dbg(f"Opening face tracking for camera: {camera_index}")
    cap = cv2.VideoCapture(camera_index)

    if face_mesh: face_mesh.close()
    face_mesh = mp.solutions.face_mesh.FaceMesh(False, 1, refine_landmarks=True)

    def show_frame():
        global frame_loop_id
        global nose_x, nose_y, nose_z, left_x, left_y, left_z, right_x, right_y, right_z

        if not cap or not cap.isOpened(): return
        ret, frame = cap.read()
        if not ret:
            frame_loop_id = image_label.after(10, show_frame)
            return

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(img_rgb)

        if results.multi_face_landmarks:
            h, w = img_rgb.shape[:2]
            lms = results.multi_face_landmarks[0].landmark
            nose, left, right = lms[1], lms[468], lms[473]

            nose_x, nose_y, nose_z = round(nose.x, 5), round(nose.y, 5), round(nose.z, 5)
            left_x, left_y, left_z = round(left.x, 5), round(left.y, 5), round(left.z, 5)
            right_x, right_y, right_z = round(right.x, 5), round(right.y, 5), round(right.z, 5)

            # Update face points dictionary
            latest_face_points["nose"] = (nose_x, nose_y, nose_z)
            latest_face_points["left_iris"] = (left_x, left_y, left_z)
            latest_face_points["right_iris"] = (right_x, right_y, right_z)

            for pt, color in zip([nose, left, right], [(0,255,0), (255,0,0), (0,0,255)]):
                x, y = int(pt.x * w), int(pt.y * h)
                cv2.circle(img_rgb, (x, y), 3, color, -1)

            if shared.debug:
                debug_text: str = (f"NOSE(x={nose_x}, y={nose_y}, z={nose_z}) ",
                                   f"LEFTEYE(x={left_x}, y={left_y}, z={left_z}) ",
                                   f"RIGHTEYE(x={right_x}, y={right_y}, z={right_z}) ")
                
                debug_label.configure(text=debug_text)
        else:
            # Clear previous values
            latest_face_points["nose"] = None
            latest_face_points["left_iris"] = None
            latest_face_points["right_iris"] = None

        if image_label.winfo_width() > 0:
            img = Image.fromarray(img_rgb)
            img.thumbnail((image_label.winfo_width(), image_label.winfo_height()), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            image_label.configure(image=img_tk)
            image_label.image = img_tk

        frame_loop_id = image_label.after(10, show_frame)

    threading.Thread(target=show_frame, daemon=True).start()

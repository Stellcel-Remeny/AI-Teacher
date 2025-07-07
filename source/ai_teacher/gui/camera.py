#
# NEW: Python face detection using Google MediaPipe
# For Remeny AI-Teacher
#

# ---[ Libraries ]--- #
from ai_teacher.resources import functions as f
from ai_teacher.resources import shared
from ai_teacher.backend import camera_backend
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

# Store latest detected face points
latest_face_points = {
    "nose": None,
    "left_iris": None,
    "right_iris": None
}

def init(win: "gui.app") -> None:
    def on_combobox_selected(cam_name: str) -> None:
        win.buttons["Next"].configure(state="enabled") # type: ignore
        # Find camera index by name
        index = dict((name, idx) for idx, name in cameras).get(cam_name)
        if index is not None:
            open_face_track(image_label, index)
        else:
            f.quit(1, f"Selected camera '{cam_name}' not found.")
    
    win.root.title("Remeny AI Teacher - Camera Trainer")
    win.banner("Camera calibrator", "Select a camera to train your Head positons.")
    win.action_bar(buttons=(("Cancel", gui.quit), ("Next", gui.not_implemented)))
    win.buttons["Next"].configure(state="disabled")
    
    cameras = camera_backend.list_cameras()
    if not cameras:
        f.quit(1, "No cameras are available. Check if you have permissions, or connect a camera if you don't have one.")
        
    camera_names = [name for (_, name) in cameras]
    
    combobox_cam_selector = gui.CTkLabelledComboBox(win.main, "Use camera:", camera_names)
    combobox_cam_selector.combobox.configure(command = on_combobox_selected) # type: ignore
    combobox_cam_selector.grid(padx=50, pady=20, sticky="w") # type: ignore
    
    instruction_label = ctk.CTkLabel(
        master=win.main,
        text="Loading...",
        font=ctk.CTkFont(size=14),
        justify="center"
    )
    instruction_label.grid(pady=(0, 5))
    
    image_frame = ctk.CTkFrame(win.main, width=500, height=500)
    image_frame.grid_propagate(False)
    image_frame.grid(pady=20)
    
    image_label = ctk.CTkLabel(image_frame, text="")
    image_label.grid(row=0, column=0, sticky="nsew")
    image_frame.rowconfigure(0, weight=1)
    image_frame.columnconfigure(0, weight=1)
    
    def on_capture() -> None:
        if None in latest_face_points.values():
            f.dbg("Face points not available yet.")
            return
        camera_backend.capture_face_points(
            [left_x, left_y, left_z],
            [right_x, right_y, right_z],
            [nose_x, nose_y, nose_z]
        )
        
    capture_button = ctk.CTkButton(win.main, text="Capture", command=on_capture)
    capture_button.grid()
    
    instruction_label.configure(text="Please select a camera from above.\nAfter selecting, instructions will appear here. For capture button, scroll down.")
    
    win.root.mainloop()

def open_face_track(image_label: "ctk.CTkLabel", camera_index: int) -> None:
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

            nose_x, nose_y, nose_z = nose.x, nose.y, nose.z
            left_x, left_y, left_z = left.x, left.y, left.z
            right_x, right_y, right_z = right.x, right.y, right.z

            for pt, color in zip([nose, left, right], [(0,255,0), (255,0,0), (0,0,255)]):
                x, y = int(pt.x * w), int(pt.y * h)
                cv2.circle(img_rgb, (x, y), 3, color, -1)

            direction = camera_backend.get_gaze_direction(nose, left, right)
            print(direction)

        if image_label.winfo_width() > 0:
            img = Image.fromarray(img_rgb)
            img.thumbnail((image_label.winfo_width(), image_label.winfo_height()), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            image_label.configure(image=img_tk)
            image_label.image = img_tk

        frame_loop_id = image_label.after(10, show_frame)

    threading.Thread(target=show_frame, daemon=True).start()

#
# NEW: Python face detection using Google MediaPipe
# For Remeny AI-Teacher
#

# ---[ Libraries ]--- #
from ai_teacher.resources import functions as f
from ai_teacher.resources import shared
from ai_teacher.backend import camera_backend
from ai_teacher.gui import gui

import customtkinter as ctk # type: ignore
import cv2
import mediapipe as mp # type: ignore
from PIL import Image, ImageTk # type: ignore

def init(win: "gui.app") -> None:
    def on_combobox_selected(cam_name: str) -> None:
        action_buttons["Next"].configure(state="enabled") # type: ignore
        # Find camera index by name
        index = dict((name, idx) for idx, name in cameras).get(cam_name)
        if index is not None:
            open_face_track(index)
        else:
            f.quit(1, f"Selected camera '{cam_name}' not found.")
    
    win.root.title("Remeny AI Teacher - Camera Trainer")
    gui.Banner(win.main, "Camera selector", "Select a camera to use with MediaPipe.")
    action_buttons = gui.ActionBar(
        win.root,
        buttons=(("Next", gui.not_implemented), ("Cancel", gui.quit))
    ).get()[1]
    
    action_buttons["Next"].configure(state="disabled") # type: ignore
    
    # Get the available cameras.
    # User should be able to select which one to use.
    cameras = camera_backend.list_cameras()
    if not cameras:
        # No cameras are available
        f.quit(1, "No cameras are available. Check if you have permissions, or connect a camera if you don't have one.")
        
    camera_names = [name for (_, name) in cameras]
    
    # Add the camera selector
    combobox_cam_selector = gui.CTkLabelledComboBox(win.main, "Use camera:", camera_names)
    combobox_cam_selector.combobox.configure(command = on_combobox_selected) # type: ignore
    combobox_cam_selector.grid(padx=50, pady=20, sticky="w") # type: ignore
    
    # Textboxes
    help_label = ctk.CTkLabel(win.main, text="/\\\n|\nSelect a camera from the dropdown above.\nYou should see another window pop up with the camera feed.")
    help_label.grid(padx=10, pady=0, sticky="w") # type: ignore
    win.root.mainloop()

def open_face_track(camera_index: int) -> None:
    """
    Opens a window to track the face using MediaPipe and the selected camera.
    Args:
        camera_name (str): The name of the camera to use for tracking.
    Returns:
        None
    """
    f.dbg(f"Opening face tracking for camera: {camera_index}")
    cap = cv2.VideoCapture(camera_index)
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(img_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Nose tip (landmark 1), Iris center (landmarks 468, 473)
                nose = face_landmarks.landmark[1]
                left_iris = face_landmarks.landmark[468]
                right_iris = face_landmarks.landmark[473]

                # Convert normalized coords to pixel coords
                h, w, _ = frame.shape
                nx, ny, nz = int(nose.x * w), int(nose.y * h), nose.z
                lix, liy, liz = int(left_iris.x * w), int(left_iris.y * h), left_iris.z
                rix, riy, riz = int(right_iris.x * w), int(right_iris.y * h), right_iris.z

                # Draw key points
                cv2.circle(frame, (nx, ny), 3, (0, 255, 0), -1)
                cv2.circle(frame, (lix, liy), 3, (255, 0, 0), -1)
                cv2.circle(frame, (rix, riy), 3, (0, 0, 255), -1)

                # Print 3D position (you can use this to calculate direction)
                print(f"Nose: ({nx}, {ny}, {nz:.2f}), Left Iris Z: {liz:.2f}, Right Iris Z: {riz:.2f}")

        cv2.imshow('Face 3D Tracking', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
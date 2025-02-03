import cv2
import os
from PIL import Image, ImageTk
from tkinter import Label, Button, messagebox
from api_service import APIService


class Camera:
    def __init__(self, root, utils, callback):
        self.root = root
        self.utils = utils
        self.callback = callback
        self.cap = None
        self.IMAGE_DIR = "captured_images"
        os.makedirs(self.IMAGE_DIR, exist_ok=True)

    def start_camera(self):
        """ Starts the camera for an existing user and enables photo capture. """
        self.utils.clear_window()
        self.utils.create_label("Look at the camera and capture your photo", 16, pady=10)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.utils.show_toast("Error", "Cannot access the camera")
            return

        self.video_label = Label(self.root)
        self.video_label.pack()

        self.update_frame()
        self.utils.create_button("Capture Photo", self.capture_photo)

    def update_frame(self):
        """ Updates the camera feed in real-time. """
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb).resize((640, 480))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.config(image=imgtk)
            self.video_label.imgtk = imgtk
            self.root.after(20, self.update_frame)

    def capture_photo(self):
        """ Captures and saves the photo, then logs in the user via face recognition. """
        ret, frame = self.cap.read()
        if ret:
            filename = os.path.join(self.IMAGE_DIR, "captured_photo.jpg")
            cv2.imwrite(filename, frame)

            # ✅ Release the camera
            self.cap.release()

            # ✅ Destroy video feed UI elements
            if hasattr(self, 'video_label'):
                self.video_label.destroy()

            self.utils.clear_window()  # ✅ Ensure UI is reset before showing the next step

            # ✅ Send captured image to backend for login
            response = APIService.login_with_face(filename)
            print("Login response:", response.get("token"))
            if response.get("token"):
                self.utils.show_toast("Success", "Login successful! Welcome back.")
                print(f"✅ Login successful! Callback function: {self.callback}")  # ✅ Debugging

                # ✅ Check if callback exists
                if callable(self.callback):
                    print("✅ Executing callback function (show_user_info)...")
                    self.root.after(1000, self.callback)  # ✅ Move to user info screen after 1 second
                else:
                    print("❌ Callback function is MISSING or Not Callable!")
            else:
                self.utils.show_toast("Error", response.get("message"))
                self.utils.create_button("Try Again", self.start_camera, 12)  # ✅ Allow retry

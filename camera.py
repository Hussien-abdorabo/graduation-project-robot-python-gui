import cv2
import os
from PIL import Image, ImageTk
from tkinter import Label, Button, messagebox

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
            messagebox.showerror("Error", "Cannot access the camera")
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
        """ Captures and saves the photo, then proceeds to registration. """
        ret, frame = self.cap.read()
        if ret:
            filename = os.path.join(self.IMAGE_DIR, "captured_photo.jpg")
            cv2.imwrite(filename, frame)
            self.cap.release()
            self.callback()  # ✅ Return to registration form

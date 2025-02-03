import cv2
import os
from PIL import Image, ImageTk
from tkinter import Label, Button, messagebox
from api_service import APIService


class Camera:
    def __init__(self, root, utils, callback):
        self.root = root
        self.utils = utils
        self.callback = callback  # ✅ Now it can be login OR registration
        self.cap = None
        self.IMAGE_DIR = "captured_images"
        os.makedirs(self.IMAGE_DIR, exist_ok=True)

    def loading_camera(self):
        """ Displays a loading message before starting the camera. """
        self.utils.clear_window()
        self.utils.create_label("📷 Loading camera...", 16, pady=10)
        # ✅ Delay starting the camera to show the loading message
        self.root.after(2000, self.start_camera)

    def start_camera(self):

        """ Starts the camera feed and displays the video feed. """

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.utils.show_toast("Error", "Cannot access the camera")
            return

        # ✅ Remove loading message before displaying the camera
        for widget in self.root.winfo_children():
            widget.destroy()

        self.utils.create_label("Look at the camera and capture your photo", 16, pady=10)

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
        """ Captures and saves the photo, then executes the callback function. """
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

            # ✅ Execute the callback function
            if callable(self.callback):
                print("✅ Executing callback function...")
                self.callback(filename)  # ✅ Pass image path to callback function
            else:
                print("❌ Callback function is missing or not callable!")

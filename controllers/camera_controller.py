# controllers/camera_controller.py
import cv2
import os


class CameraController:
    def __init__(self, callback):
        self.callback = callback
        self.cap = None
        self.IMAGE_DIR = "assets/captured_images"
        os.makedirs(self.IMAGE_DIR, exist_ok=True)

    def start_camera(self):
        """ Starts the camera feed and ensures it's properly initialized. """
        if self.cap is not None and self.cap.isOpened():
            print("✅ Camera is already open.")
            return True  # ✅ Avoid opening multiple instances

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("❌ Camera failed to open")
            self.cap = None  # ✅ Prevent access to an invalid camera instance
            return False

        print("✅ Camera successfully opened.")
        return True

    def capture_photo(self, image_path="assets/captured_images/captured_photo.jpg"):
        """ Ensures camera is open before capturing and captures instantly. """
        if self.cap is None or not self.cap.isOpened():
            print("❌ Camera is not open! Cannot capture photo.")
            return None

        ret, frame = self.cap.read()
        if not ret:
            print("❌ Failed to capture frame")
            return None

        cv2.imwrite(image_path, frame)
        print(f"✅ Photo saved to {image_path}")

        return image_path  # ✅ Do NOT release camera here, let `exit_application()` handle it



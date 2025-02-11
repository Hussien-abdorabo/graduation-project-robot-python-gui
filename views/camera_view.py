from tkinter import Label, Button
import cv2
from PIL import Image, ImageTk, ImageDraw


class CameraView:
    def __init__(self, root, utils, controller):
        self.root = root
        self.utils = utils
        self.controller = controller
        self.video_label = None  # ✅ Initialize in __init__

    def show_camera_loading(self):
        """ Displays loading message before camera opens """
        self.utils.clear_window()
        self.utils.create_label("📷 Loading camera...", 16, pady=10)
        self.utils.speak_arabic("Loading camera")
        self.root.after(1000, self.show_camera_feed)

    def show_camera_feed(self):
        """ Displays the camera UI and starts video stream """
        if not self.controller.start_camera():
            self.utils.show_toast("Error", "Cannot access the camera")
            return

        self.utils.clear_window()
        self.utils.create_label("Look at the camera and capture your photo", 16, pady=10)

        # ✅ Always reinitialize video_label
        self.video_label = Label(self.root)
        self.video_label.pack()

        self.update_frame()  # ✅ Start updating frames

        # ✅ Capture button added AFTER the camera loads
        self.utils.create_button("Capture Photo", self.capture_photo, 20)


    def update_frame(self):
        """ Continuously updates the camera feed with rounded corners. """
        if not hasattr(self, "video_label") or not self.video_label.winfo_exists():
            print("❌ Video label was destroyed. Stopping frame update.")
            return  # ✅ Prevent updating if the label is missing

        ret, frame = self.controller.cap.read()
        if ret:
            # ✅ Resize frame
            frame = cv2.resize(frame, (640, 480))

            # ✅ Convert BGR to RGB for Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # ✅ Convert frame to PIL Image
            img = Image.fromarray(frame_rgb)

            # ✅ Create a rounded rectangle mask
            mask = Image.new("L", (640, 480), 0)
            draw = ImageDraw.Draw(mask)
            border_radius = 40  # Adjust this for more or less rounded corners
            draw.rounded_rectangle((0, 0, 640, 480), radius=border_radius, fill=255)

            # ✅ Apply the mask
            img.putalpha(mask)

            # ✅ Convert to ImageTk format
            imgtk = ImageTk.PhotoImage(img)

            if self.video_label.winfo_exists():  # ✅ Ensure the label still exists before updating
                self.video_label.config(image=imgtk)
                self.video_label.imgtk = imgtk
                self.root.after(20, self.update_frame)  # ✅ Keep updating frames

    def capture_photo(self):
        """ Captures the photo and stops updating frames. """
        if self.controller.cap is None or not self.controller.cap.isOpened():
            print("❌ Camera is not open! Cannot capture photo.")
            return

        # ✅ Capture photo first before stopping update_frame
        filename = self.controller.capture_photo()

        if filename:
            print("✅ Photo captured successfully!")
            self.utils.show_toast("Success", "Photo captured successfully!")
            self.controller.callback(filename)  # ✅ Trigger the callback
        else:
            self.utils.show_toast("Error", "Failed to capture photo")

        # ✅ Stop camera feed after capturing
        if self.controller.cap:
            self.controller.cap.release()
            self.controller.cap = None  # ✅ Ensure no lingering camera instance

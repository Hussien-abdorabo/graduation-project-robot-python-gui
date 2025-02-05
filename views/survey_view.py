import os
import tkinter as tk
import cv2
from PIL import Image, ImageTk  # ✅ Fix missing import


class SurveyView:
    def __init__(self, root, utils, controller, doctor_view,app):
        self.root = root
        self.utils = utils
        self.controller = controller
        self.doctor_view = doctor_view
        self.image_path = None  # ✅ Store image path globally
        self.app = app

    def ask_how_are_you(self):
        """ Ask how the user is feeling today. """
        self.utils.clear_window()
        self.utils.create_label("How are you doing today?", 16, pady=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        self.utils.create_button("Good", self.ask_skin_disease, 10, button_frame, "left", 20)
        self.utils.create_button("Bad", lambda: self.show_support(self.ask_skin_disease), 10, button_frame, "left", 20)
    def show_support(self, next_function):
        """ Displays support message. """
        self.utils.clear_window()
        self.utils.create_label("Don't worry, I am here for you!", 16, pady=20)
        self.root.after(1000, next_function)
    def ask_skin_disease(self):
        """ Ask if the user has a skin disease. """
        self.utils.clear_window()
        self.utils.create_label("Do you suffer from any skin diseases?", 16, pady=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        self.utils.create_button("Yes", self.skin_photo_availability, 10, button_frame, "left", 20)
        self.utils.create_button("No", self.continue_with_diagnosing_or_not, 10, button_frame, "left", 20)
    def continue_with_diagnosing_or_not(self):
        """ Ask user if they want to continue without a skin photo. """
        self.utils.clear_window()
        self.utils.create_label(
            "I am here to help you! Do you want to continue diagnosing or no?",
            14
        )
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        self.utils.create_button("Yes", self.start_scan_process, frame=button_frame, side="left", padx=20)
        self.utils.create_button("No", self.app.exit_application, frame=button_frame, side="left", padx=20)

    def why_here(self):
        """ Exits the application """
        self.utils.clear_window()
        self.utils.create_label("✨ I'm an AI Model designed to help classify and diagnose the skin dresses! You want to continue with me? ✨", 16, "bold")
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        self.utils.create_button("Yes", self.skin_photo_availability, frame=button_frame, side="left", padx=20)
        self.utils.create_button("No", self.app.exit_application, frame=button_frame, side="left", padx=20)
    def skin_photo_availability(self):
        """ Ask if the user can provide a picture of the disease. """
        self.utils.clear_window()
        self.utils.create_label("Can you provide a picture of this disease so that I can help you?", 14)

        button_frame = tk.Frame(self.root)
        button_frame.pack()
        self.utils.create_button("Yes", self.start_scan_process, frame=button_frame, side="left", padx=20)
        self.utils.create_button("No", self.doctor_view.show_qr_code, frame=button_frame, side="left", padx=20)

    def start_scan_process(self):
        """ Displays loading message, then opens the camera for preview. """
        self.utils.clear_window()
        self.utils.create_label("📷 Loading camera...", 16, pady=10)
        self.root.after(1000, self.show_camera_feed)
    def show_camera_feed(self):
        """ Opens the camera stream for preview before capturing. """
        if not self.controller.start_scan_process():
            self.utils.show_toast("Error", "Cannot access the camera")
            return

        self.utils.clear_window()
        self.utils.create_label("Look at the camera and capture your photo", 16, pady=10)

        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        self.update_frame()  # ✅ Start updating frames in the UI

        # ✅ Now we create a manual button for capturing
        self.utils.create_button("Capture Photo", self.capture_photo, 20)
    def update_frame(self):
        """ Updates the camera feed and stores the latest frame for instant capture. """
        if not self.controller.camera_controller.cap or not self.controller.camera_controller.cap.isOpened():
            print("❌ Camera is not open! Cannot update frame.")
            return

        ret, frame = self.controller.camera_controller.cap.read()
        if ret:
            self.last_displayed_frame = frame  # ✅ Store the last displayed frame

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb).resize((640, 480))
            imgtk = ImageTk.PhotoImage(image=img)

            if hasattr(self, "video_label") and self.video_label.winfo_exists():
                self.video_label.config(image=imgtk)
                self.video_label.imgtk = imgtk
                self.root.after(20, self.update_frame)  # ✅ Keep updating frames

    def capture_photo(self):
        """ Captures the last displayed frame when the user clicks the button. """
        if not hasattr(self, "last_displayed_frame"):
            self.utils.show_toast("Error", "❌ No frame available for capture!")
            return

        # ✅ Stop updating the camera feed
        self.root.after_cancel(self.update_frame)

        # ✅ Save the last displayed frame instead of capturing a new one
        image_path = os.path.join(self.controller.DISEASE_IMAGE_DIR, "disease_photo.jpg")
        cv2.imwrite(image_path, self.last_displayed_frame)

        print(f"✅ Instant Capture: Photo saved to {image_path}")

        # ✅ Properly release the camera after capture
        if self.controller.camera_controller.cap:
            self.controller.camera_controller.cap.release()
            self.controller.camera_controller.cap = None  # ✅ Ensure the camera instance is reset

        self.image_path = image_path  # ✅ Store the path
        self.send_image_for_diagnosis()

    def send_image_for_diagnosis(self):
        """ Sends the captured image to the AI model for diagnosis. """
        if not self.image_path or not os.path.exists(self.image_path):
            self.utils.show_toast("Error", "❌ No valid image captured!")
            return

        # ✅ Extra safety: Close the camera if it's still open
        if self.controller.camera_controller.cap:
            self.controller.camera_controller.cap.release()
            self.controller.camera_controller.cap = None

        self.utils.clear_window()
        self.utils.create_label("🔍 Sending image for diagnosis...", 14)

        response = self.controller.diagnose_skin_disease(self.image_path)

        if response.get("status") == "success":
            self.show_prediction_results(response.get("message"))
        else:
            self.utils.show_toast("Error", response.get("message", "Unknown error"))

    def show_prediction_results(self, diagnosis_response):
        """ Displays AI-generated diagnosis and recommendations, including doctor info. """
        self.utils.clear_window()

        # Extracting diagnosis information
        if isinstance(diagnosis_response, str):
            disease = diagnosis_response
            treatment = "No specific treatment recommended."
        else:
            disease = diagnosis_response.get("condition", "Unknown")
            treatment = diagnosis_response.get("explanation", "Unknown")

        # Retrieve doctor details if available
        doctor_data = self.controller.get_doctor_data()
        doctor_name = doctor_data.get("name", "Dr. John Smith")
        doctor_phone = doctor_data.get("phone", "+123456789")
        doctor_location = doctor_data.get("location", "123 Health St, Medical City")

        # Display diagnosis result
        self.utils.create_label(f"🔍 Diagnosis Result: {disease}", 16, "bold",pady=5)
        self.utils.create_label(f"💊 Treatment: {treatment}", 14,pady=5)
        self.utils.create_label("👨‍⚕️ Doctor Contact:", 14, "bold",pady=5)
        self.utils.create_label(f"🩺 Name: {doctor_name}", 14,pady=5)
        self.utils.create_label(f"📞 Phone: {doctor_phone}", 14,pady=5)
        self.utils.create_label(f"📍 Location: {doctor_location}", 14,pady=5)

        # ✅ Exit or continue buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        self.doctor_view.ask_user_to_continue()


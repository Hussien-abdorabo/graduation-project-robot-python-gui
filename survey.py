import tkinter as tk
from tkinter import Label, Button
import os
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox
from doctor_consultation import DoctorConsultation
from qr_assistant import QRAssistant
from api_service import APIService  # ✅ Import APIService


class Survey:
    def __init__(self, root, utils, camera,ApiService, next_step):
        self.root = root
        self.utils = utils
        self.camera = camera
        self.next_step = next_step
        self.photo_count = 0
        self.DISEASE_IMAGE_DIR = "diseases-photos"
        self.consultation = DoctorConsultation(root, utils)  # ✅ Use new module
        self.qr_assistant = QRAssistant(root, utils, self.start_scan_process)  # ✅ Use new module
        self.api_service = ApiService

        os.makedirs(self.DISEASE_IMAGE_DIR, exist_ok=True)

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
        self.root.after(2000, next_function)

    def ask_skin_disease(self):
        """ Ask if user has a skin disease. """
        self.utils.clear_window()
        self.utils.create_label("Do you suffer from any skin diseases?", 16, pady=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        self.utils.create_button("Yes", self.skin_photo_avalibilty, 10, button_frame, "left", 20)
        self.utils.create_button("No", self.continue_with_diagnosing_or_not, 10, button_frame, "left", 20)

    def continue_with_diagnosing_or_not(self):
        """ Asks if the user can provide a picture of the disease. """
        self.utils.clear_window()
        self.utils.create_label("So how can i help you iam here to help you if you have any skin diseases Want to continue or not?", 14)
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        self.utils.create_button("Yes", self.start_scan_process, frame=button_frame, side="left", padx=20)
        self.utils.create_button("No", self.qr_assistant.exit_application, frame=button_frame, side="left",
                                 padx=20)

    def skin_photo_avalibilty(self):
        """ Asks if the user can provide a picture of the disease. """
        self.utils.clear_window()
        self.utils.create_label("Can you provide a picture of this disease so that I can help you?", 14)

        button_frame = tk.Frame(self.root)
        button_frame.pack()
        self.utils.create_button("Yes", self.start_scan_process, frame=button_frame, side="left", padx=20)
        self.utils.create_button("No", self.qr_assistant.show_qr_code_for_co_pilot, frame=button_frame, side="left",
                                 padx=20)


    def start_scan_process(self):
        """ Allows the user to capture a single image of the disease before AI diagnosis. """
        self.utils.clear_window()
        self.loading_camera()
    def loading_camera(self):
        """ Displays a loading message before starting the camera. """
        self.utils.clear_window()
        self.utils.create_label("📷 Loading camera...", 16, pady=10)
        # ✅ Delay starting the camera to show the loading message
        self.root.after(1000, self.capture_photo)

    def capture_photo(self):
        self.utils.create_label("Please capture an image of the disease for better diagnosis.", 14)
        """ Opens the camera and allows the user to capture a single disease-related photo. """
        self.camera.cap = cv2.VideoCapture(0)

        if not self.camera.cap.isOpened():
            self.utils.show_toast("Error", "Cannot access the camera")
            return

        self.video_label = Label(self.root)
        self.video_label.pack()

        self.update_frame()
        self.utils.create_button("Capture Photo", self.capture_and_store)

    def update_frame(self):
        """ Updates the camera feed in real-time. """
        ret, frame = self.camera.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb).resize((640, 480))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.config(image=imgtk)
            self.video_label.imgtk = imgtk
            self.root.after(20, self.update_frame)

    def capture_and_store(self):
        """ Captures and stores a single image, then proceeds to diagnosis. """
        ret, frame = self.camera.cap.read()
        if ret:
            filename = os.path.join(self.DISEASE_IMAGE_DIR, "disease_photo.jpg")
            cv2.imwrite(filename, frame)
            self.camera.cap.release()
            self.send_image_for_diagnosis(filename)  # ✅ Send only one image for diagnosis

    def send_image_for_diagnosis(self, image_path):
        """ Sends the captured image to the backend AI model for diagnosis. """
        self.utils.clear_window()
        self.utils.create_label("🔍 Sending image for diagnosis...", 14)
        print(f"Sending image for diagnosis: {image_path}")

        # ✅ Send single image to the API
        response = APIService.diagnose_skin_disease(image_path)  # ✅ Already a dict, no need for .json()

        print(f"API Response: {response}")  # ✅ Debugging

        if response.get("status") == "success":  # ✅ Correctly access dictionary keys
            self.show_prediction_results(response.get("message"))
        else:
            self.utils.show_toast("Error", response.get("message", "Unknown error"))

    def show_prediction_results(self, diagnosis_response):
        """ Displays AI-generated diagnosis and recommendations, then asks user if they want to continue. """
        self.utils.clear_window()
        disease = "Unknown"
        treatment = "Unknown"
        doctor_name = self.api_service.doctor_data.get("name", "Dr. John Smith")
        doctor_phone = self.api_service.doctor_data.get("phone", "+123456789")
        doctor_location = self.api_service.doctor_data.get("location", "123 Health St, Medical City")
        print(f"Diagnosis Response: {diagnosis_response}")  # ✅ Debugging
        #  check if it's a string or array
        if isinstance(diagnosis_response, str):
            self.utils.create_label(f"🔍 Diagnosis Result: {diagnosis_response}", 16, "bold")
            self.utils.create_label("👨‍⚕️ Doctor Contact:", 14, "bold")
            self.utils.create_label(f"🩺Name: {doctor_name}", 14)
            self.utils.create_label(f"📞 Phone: {doctor_phone}", 14)
            self.utils.create_label(f"📍 Location: {doctor_location}", 14)
        else:
            disease = diagnosis_response["condition"] if "condition" in diagnosis_response else "Unknown"
            treatment = diagnosis_response["explanation"] if "explanation" in diagnosis_response else "Unknown"
            doctor_name = diagnosis_response.get("doctor_name", "Dr. John Smith")
            doctor_phone = diagnosis_response.get("doctor_phone", "+123456789")
            doctor_location = diagnosis_response.get("doctor_location", "123 Health St, Medical City")
            self.utils.create_label(f"🔍 Diagnosis Result: {disease}", 16, "bold")
            self.utils.create_label(f"💊 Treatment: {treatment}", 14)
            self.utils.create_label("👨‍⚕️ Doctor Contact:", 14, "bold")
            self.utils.create_label(f"🩺 {doctor_name}", 14)
            self.utils.create_label(f"📞 Phone: {doctor_phone}", 14)
            self.utils.create_label(f"📍 Location: {doctor_location}", 14)

            # ✅ Ask user if they want to continue
        self.consultation.ask_user_to_continue()




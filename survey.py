import tkinter as tk
from tkinter import Label, Button
import os
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox
from doctor_consultation import DoctorConsultation
from qr_assistant import QRAssistant

class Survey:
    def __init__(self, root, utils, camera, next_step):
        self.root = root
        self.utils = utils
        self.camera = camera
        self.next_step = next_step
        self.photo_count = 0
        self.DISEASE_IMAGE_DIR = "diseases-photos"
        self.consultation = DoctorConsultation(root, utils)  # ✅ Use new module
        self.qr_assistant = QRAssistant(root, utils, self.start_scan_process)  # ✅ Use new module

    # def skin_photo_avalibilty(self):
    #     """ Ask user if they can provide a picture. """
    #     self.qr_assistant.ask_for_image()  # ✅ Use QRAssistant instead
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
        self.utils.create_button("No", self.ask_how_are_you, 10, button_frame, "left", 20)

    def skin_photo_avalibilty(self):
        """ Asks if the user can provide a picture of the disease. """
        self.utils.clear_window()
        self.utils.create_label("Can you provide a picture of this disease so that I can help you?", 14)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        self.utils.create_button("Yes", self.start_scan_process, frame=button_frame, side="left", padx=20)
        self.utils.create_button("No", self.qr_assistant.show_qr_code_for_co_pilot, frame=button_frame, side="left", padx=20)

    def start_scan_process(self):
        """ Allows the user to capture three disease-related photos before AI diagnosis. """
        self.photo_count = 0  # Reset counter
        self.utils.clear_window()
        self.utils.create_label("Please capture 3 images of the disease for better diagnosis.", 14)
        self.capture_more_photos()

    def capture_more_photos(self):
        """ Opens camera for capturing disease photos. """
        self.camera.cap = cv2.VideoCapture(0)

        if not self.camera.cap.isOpened():
            messagebox.showerror("Error", "Cannot access the camera")
            return

        self.video_label = Label(self.root)
        self.video_label.pack()

        self.progress_label = Label(self.root, text=f"Captured: {self.photo_count}/3", font=("Helvetica", 14))
        self.progress_label.pack()

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
        """ Captures and stores an image, updating progress. """
        ret, frame = self.camera.cap.read()
        if ret:
            filename = os.path.join(self.DISEASE_IMAGE_DIR, f"disease_photo_{self.photo_count+1}.jpg")
            cv2.imwrite(filename, frame)
            self.photo_count += 1
            self.progress_label.config(text=f"Captured: {self.photo_count}/3")

        if self.photo_count == 3:
            self.camera.cap.release()
            self.simulate_prediction()

    def simulate_prediction(self):
        """ Simulates AI processing for diagnosis. """
        self.utils.clear_window()
        self.utils.create_label("Processing images through AI model...", 14)
        self.root.after(2000, self.show_prediction_results)

    def show_prediction_results(self):
        """ Displays AI-generated diagnosis and recommendations, then asks user if they want to continue. """
        self.utils.clear_window()

        # 🏥 Diagnosis & Recommendations
        self.utils.create_label("🔍 Diagnosis Result: Skin Infection", 16, "bold")
        self.utils.create_label("💊 Suggested Medicine: Antibiotic Cream", 14)
        self.utils.create_label("👨‍⚕️ Doctor Contact:", 14, "bold")
        self.utils.create_label("🩺 Dr. John Smith", 14)
        self.utils.create_label("📞 Phone: +123456789", 14)
        self.utils.create_label("📍 Location: 123 Health St, Medical City", 14)

        # ✅ Ask user if they want to continue
        self.consultation.ask_user_to_continue()

        
        

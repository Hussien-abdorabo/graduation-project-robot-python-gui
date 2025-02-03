import os
import tkinter as tk
from tkinter import Entry, Label, Button, messagebox
from camera import Camera
import re  # ✅ For generating a slug from the user's name & email
from api_service import APIService


class Register:
    def __init__(self, root, utils, show_user_info):
        self.root = root
        self.utils = utils
        self.name_entry = None
        self.email_entry = None
        self.password1_entry = None
        self.password2_entry = None
        self.captured_image_path = None  # ✅ Store captured image path
        self.user_photos_dir = "user_photos"
        os.makedirs(self.user_photos_dir, exist_ok=True)  # ✅ Ensure folder exists
        self.user_data = {}  # ✅ Store user data before clearing UI
        self.show_user_info = show_user_info

        # ✅ Camera initialized but will only start when user clicks "Capture"
        self.camera = Camera(root, utils, self.handle_registration_photo)

    def start_camera(self):
        """ Saves user input before opening the camera. """
        self.user_data["name"] = self.name_entry.get().strip()
        self.user_data["email"] = self.email_entry.get().strip()
        self.user_data["password1"] = self.password1_entry.get().strip()
        self.user_data["password2"] = self.password2_entry.get().strip()

        if not self.user_data["name"] or not self.user_data["email"]:
            self.utils.show_toast("Error", "Please enter your name and email before capturing a photo.")
            return

        self.utils.clear_window()  # ✅ Now safe because data is stored
        self.camera.loading_camera()

    def handle_registration_photo(self, image_path):
        """ Handles the captured photo and completes the registration. """
        self.captured_image_path = image_path  # ✅ Store the captured image path
        self.show_registration_form()  # ✅ Call registration after capturing photo

    def register_user(self):
        """ Validates and registers the user with the backend API. """
        name = self.user_data["name"]
        email = self.user_data["email"]
        password1 = self.user_data["password1"]
        password2 = self.user_data["password2"]

        if not self.captured_image_path:
            self.utils.show_toast("Error", "Please capture a profile photo!")
            return

        # ✅ Send data to the backend API
        response = APIService.register_user(name, email, password1, password2,"patient", self.captured_image_path)
        print(f"🔍 Registration Response 2: {response}")
        if response.get("success"):
            self.utils.show_toast("Success", "Registration successful! You are now logged in.")
            APIService.token = response.get("token")  # ✅ Store token globally
            APIService.user_data = response.get("user")  # ✅ Store user data globally
            self.show_user_info()
        else:
            self.utils.clear_window()
            self.utils.show_toast("Error", response.get("message"))
            self.utils.create_button("Try Again", self.show_registration_form, 12)

    def show_registration_form(self):
        """ Displays the registration form for new users. """
        self.utils.clear_window()
        self.utils.create_label("📝 User Registration", 18, "bold")

        # Restore user-filled data (if any)
        name_value = self.user_data.get("name", "")
        email_value = self.user_data.get("email", "")
        password1_value = self.user_data.get("password1", "")
        password2_value = self.user_data.get("password2", "")

        # ✅ Name Field
        Label(self.root, text="Full Name:", font=("Helvetica", 14)).pack(pady=5)
        self.name_entry = Entry(self.root, font=("Helvetica", 14), width=30)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, name_value)  # ✅ Restore previous value

        # ✅ Email Field
        Label(self.root, text="Email Address:", font=("Helvetica", 14)).pack(pady=5)
        self.email_entry = Entry(self.root, font=("Helvetica", 14), width=30)
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, email_value)  # ✅ Restore previous value

        # ✅ Password Fields
        Label(self.root, text="Password:", font=("Helvetica", 14)).pack(pady=5)
        self.password1_entry = Entry(self.root, font=("Helvetica", 14), width=30, show="*")
        self.password1_entry.pack(pady=5)
        self.password1_entry.insert(0, password1_value)  # ✅ Restore previous value

        Label(self.root, text="Confirm Password:", font=("Helvetica", 14)).pack(pady=5)
        self.password2_entry = Entry(self.root, font=("Helvetica", 14), width=30, show="*")
        self.password2_entry.pack(pady=5)
        self.password2_entry.insert(0, password2_value)  # ✅ Restore previous value

        # ✅ Capture Profile Photo Button
        Button(self.root, text="📷 Capture Profile Photo", command=self.start_camera, font=("Helvetica", 14),
               bg="#4CAF50", fg="white").pack(pady=10)

        # ✅ Show captured image if available
        if self.captured_image_path:
            self.utils.display_image(self.captured_image_path, 200, 200)

        # ✅ Register Button
        Button(self.root, text="Register", command=self.register_user, font=("Helvetica", 14), bg="#008CBA",
               fg="white").pack(pady=10)
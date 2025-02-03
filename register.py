import os
import tkinter as tk
from tkinter import Entry, Label, Button, messagebox
from camera import Camera
import re  # ✅ For generating a slug from the user's name & email
from api_service import APIService

class Register:
    def __init__(self, root, utils):
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

        # ✅ Camera initialized but will only start when user clicks "Capture"
        self.camera = Camera(root, utils, self.capture_photo)

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
        self.camera.start_camera()

    def capture_photo(self):
        """ Saves the captured image and returns to registration form. """
        name = self.user_data.get("name", "").strip()
        email = self.user_data.get("email", "").strip()

        # ✅ Generate a slug from name & email
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', f"{name}-{email}").lower()
        image_filename = f"{slug}.jpg"
        image_path = os.path.join(self.user_photos_dir, image_filename)

        # ✅ Move the captured image to `user_photos/`
        if os.path.exists("captured_images/captured_photo.jpg"):
            os.rename("captured_images/captured_photo.jpg", image_path)
            self.captured_image_path = image_path  # ✅ Store new image path
            self.utils.show_toast("Success", "Profile photo saved successfully!")
        else:
            self.utils.show_toast("Error", "Photo capture failed!")

        # ✅ Reload registration form with previous user input
        self.show_registration_form()

    def register_user(self):
        """ Validates and registers the user with the backend API. """
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password1 = self.password1_entry.get().strip()
        password2 = self.password2_entry.get().strip()

        if not name or not email or not password1 or not password2:
            self.utils.show_toast("Error", "All fields are required!")
            return

        if password1 != password2:
            self.utils.show_toast("Error", "Passwords do not match!")
            return

        if not self.captured_image_path:
            self.utils.show_toast("Error", "Please capture a profile photo!")
            return

        # ✅ Send data to the backend API
        response = APIService.register_user(name, email, password1, self.captured_image_path)

        if response.get("success"):
            self.utils.show_toast("Success", "Registration successful! You are now logged in.")
            APIService.token = response.get("token")  # ✅ Store token globally
        else:
            self.utils.show_toast("Error", response.get("message"))

# controllers/register_controller.py
import os
from models.api_service import APIService


class RegisterController:
    def __init__(self, utils, show_user_info, camera_controller):
        self.utils = utils
        self.user_data = {}
        self.captured_image_path = None
        self.user_photos_dir = "assets/user_photos"
        os.makedirs(self.user_photos_dir, exist_ok=True)
        self.show_user_info = show_user_info
        self.camera_controller = camera_controller  # ✅ Camera controller to manage the camera actions

    def save_user_data(self, name, email, password1, password2, image_path=""):
        """ Stores user input before opening the camera """
        self.user_data = {
            "name": name.strip(),
            "email": email.strip(),
            "password1": password1.strip(),
            "password2": password2.strip(),
            "photo": image_path  # ✅ Store the image path for pre-filling the form
        }

        if not self.user_data["name"] or not self.user_data["email"]:
            self.utils.show_toast("Error", "Please enter your name and email before capturing a photo.")
            return False

        return True  # ✅ Return success for validation check

    def handle_registration_photo(self, image_path):
        """ Handles the captured photo and returns to the registration form. """
        self.captured_image_path = image_path  # ✅ Store the image path correctly
        self.user_data["photo"] = image_path  # ✅ Store the path inside user_data too
        return self.user_data  # ✅ Ensure data is returned for pre-filling the form

    def register_user(self):
        """ Sends user data and image to API for registration """
        if not self.captured_image_path:
            self.utils.show_toast("Error", "Please capture a profile photo!")
            return

        response = APIService.register_user(
            self.user_data["name"], self.user_data["email"],
            self.user_data["password1"], self.user_data["password2"],
            "patient", self.captured_image_path
        )

        if response.get("success"):
            self.utils.show_toast("Success", "Registration successful! You are now logged in.")
            APIService.token = response.get("token")
            APIService.user_data = response.get("user")
            self.show_user_info()
        else:
            self.utils.clear_window()
            self.handle_registration_errors(response)

    def handle_registration_errors(self, response):
        """ Extracts and displays validation errors from the API response """
        error_messages = []
        print(response["errors"])
        print("--------")
        print(response["errors"].items())

        if "errors" in response:
            for field, messages in response["errors"].items():
                print(f"Field: {field}, Messages: {messages}")
                error_messages.append(f"{field.capitalize()}: {', '.join(messages)}")

        error_text = "\n".join(error_messages) if error_messages else "Registration failed. Please try again."

        self.utils.show_toast("Error", error_text)

        # ✅ Restore the form with previously entered data and captured image
        self.utils.create_button("Try Again", lambda: self.retry_registration(), 12)

    def retry_registration(self):
        print("Retrying registration... :")
        print(self.user_data)
        print("-----------")
        """ Restores the registration form with previously entered data """
        if hasattr(self, 'register_view'):
            self.register_view.show_registration_form(prefill_data=self.user_data)
        else:
            print("❌ Error: `register_view` is not defined in `RegisterController`")

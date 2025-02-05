import os
import shutil

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from models.api_service import APIService
from models.user_service import UserService
from models.utils import Utils
from controllers.camera_controller import CameraController
from controllers.survey_controller import SurveyController
from controllers.register_controller import RegisterController
from controllers.qr_controller import QRController
from controllers.doctor_controller import DoctorController
from views.camera_view import CameraView
from views.survey_view import SurveyView
from views.register_view import RegisterView
from views.qr_view import QRView
from views.doctor_view import DoctorView


class DrRobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dr. Robot - Skin Disease Diagnosis")
        self.root.geometry("900x600")
        self.style = ttk.Style()
        self.style.theme_use("superhero")

        self.utils = Utils(root)
        self.user_service = UserService()

        # ✅ Initialize separate controllers for login & registration
        self.camera_controller_login = CameraController(self.handle_login_photo)
        self.camera_controller_register = CameraController(self.handle_registration_photo)  # ✅ Fixed reference

        # ✅ Initialize other controllers
        self.survey_controller = SurveyController(self.camera_controller_login)
        self.register_controller = RegisterController(self.utils, self.show_user_info, self.camera_controller_register)
        self.qr_controller = QRController(self.utils)
        self.doctor_controller = DoctorController(self.utils)

        # ✅ Initialize Views with correct controllers
        self.camera_view_login = CameraView(root, self.utils, self.camera_controller_login)
        self.camera_view_register = CameraView(root, self.utils, self.camera_controller_register)
        self.doctor_view = DoctorView(root, self.utils, self.doctor_controller, self)
        self.survey_view = SurveyView(root, self.utils, self.survey_controller, self.doctor_view, self)
        self.register_view = RegisterView(root, self.utils, self.register_controller, self.camera_view_register)
        self.qr_view = QRView(root, self.utils, self.qr_controller)
        self.register_controller.register_view = self.register_view  # ✅ Fix reference issue

        self.main_window()

    def main_window(self):
        """ Displays the main welcome screen. """
        self.utils.clear_window()
        self.utils.create_label("Welcome to Dr.Robot", 24, pady=20, weight="bold")
        self.utils.create_button("Start", self.ask_new_user, width=15, bootstyle="primary")

    def ask_new_user(self):
        """ Ask if the user is new. """
        self.utils.clear_window()

        # ✅ Create a frame for alignment (this ensures the label and buttons are closer together)
        container_frame = ttk.Frame(self.root)
        container_frame.pack(expand=True)  # Centers everything vertically

        # ✅ Label inside the container (pady reduced to keep it close to the buttons)
        label = ttk.Label(container_frame, text="Are you a new user?", font=("Helvetica", 16))
        label.pack(pady=10)  # ✅ Reduce padding to keep it closer to buttons

        # ✅ Create a single frame for buttons (inside the same container)
        button_frame = ttk.Frame(container_frame)
        button_frame.pack(pady=60)  # ✅ Ensure buttons are just below the label

        # ✅ Create buttons inside button_frame to align in a row
        btn_yes = ttk.Button(button_frame, text="Yes", command=self.register_view.show_registration_form, width=15,
                             bootstyle="success")
        btn_yes.pack(side="left", padx=10)

        btn_no = ttk.Button(button_frame, text="No", command=self.destroy_buttons, width=15, bootstyle="danger")
        btn_no.pack(side="left", padx=10)

    def destroy_buttons(self):
        """ Destroys all buttons in the main window and opens the login camera. """
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.destroy()
        self.utils.clear_window()
        self.camera_view_login.show_camera_loading()  # ✅ Show login camera view

    def handle_login_photo(self, image_path):
        """ Handles photo capture for login. """
        response = APIService.login_with_face(image_path)
        if response.get("token"):
            self.utils.show_toast("Success", "Login successful! Welcome back.")
            self.show_user_info()
        else:
            self.utils.clear_window()
            self.utils.show_toast("Error", response.get("message"))
            self.utils.create_button("Try Again", self.camera_view_login.show_camera_loading, width=12, bootstyle="danger")

    def handle_registration_photo(self, image_path):
        """ Handles photo capture for registration and returns to the form. """
        self.register_controller.handle_registration_photo(image_path)  # ✅ Correctly store captured image
        self.register_view.show_registration_form(prefill_data=self.register_controller.user_data)  # ✅ Return to form

    def show_user_info(self):
        """ Displays user info after login in a properly organized way. """
        self.utils.clear_window()

        if APIService.user_data:
            user = APIService.user_data

            # ✅ Main container for proper centering
            container_frame = ttk.Frame(self.root)
            container_frame.pack(expand=True, fill="both")

            # ✅ Profile Image (Rounded)
            image_frame = ttk.Frame(container_frame)
            image_frame.pack(pady=10)
            self.utils.display_image("assets/captured_images/captured_photo.jpg", 220, 220)  # ⬆️ Increased size

            # ✅ User Info (Larger Font)
            user_info_frame = ttk.Frame(container_frame)
            user_info_frame.pack(pady=5)
            self.utils.create_label(f"👤 Username: {user['name']}", 18, weight="bold", pady=5)  # ⬆️ Increased font size
            self.utils.create_label(f"📧 Email: {user['email']}", 18, pady=5)

            # ✅ Welcome Message (Larger Font)
            welcome_frame = ttk.Frame(container_frame)
            welcome_frame.pack(pady=10)
            self.utils.create_label(f"🎉 Welcome, {user['name']}!", 20, "bold", pady=8)  # ⬆️ Increased font

            # ✅ Ensure the button is at the bottom of the screen
            button_frame = ttk.Frame(self.root)
            button_frame.pack(side="bottom", pady=20)
            self.utils.create_button("Next", self.survey_view.ask_how_are_you, width=15, frame=button_frame,
                                     bootstyle="info")

        else:
            self.utils.show_toast("Error", "User data not found! Please try again.")

    def exit_application(self):
        """ Resets all data and redirects to the main screen without opening a new window. """
        # ✅ Release all camera instances before exiting
        if self.camera_controller_login.cap:
            self.camera_controller_login.cap.release()
            self.camera_controller_login.cap = None

        if self.camera_controller_register.cap:
            self.camera_controller_register.cap.release()
            self.camera_controller_register.cap = None

        # ✅ Clear stored user and doctor data
        APIService.token = None
        APIService.user_data = {}

        # ✅ Delete captured images and other temporary files
        image_dirs = ["assets/captured_images", "assets/user_photos", "assets/diseases-photos"]
        for dir_path in image_dirs:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)  # Remove directory and all its contents
                os.makedirs(dir_path)  # Recreate an empty directory

        # ✅ Clear the screen and return to the main window
        self.utils.clear_window()
        self.utils.create_label("✨ Thank you for using Dr. Robot! ✨", 16, "bold")

        # ✅ Redirect to the main screen after a delay
        self.root.after(3000, self.main_window)  # ✅ Call main window from app instance


# Run the app
root = ttk.Window(themename="superhero")
app = DrRobotApp(root)
root.mainloop()

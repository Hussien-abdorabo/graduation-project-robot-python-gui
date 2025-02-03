import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from api_service import APIService
from camera import Camera
from user_service import UserService
from survey import Survey
from utils import Utils
from register import Register

class DrRobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dr. Robot - Skin Disease Diagnosis")
        self.root.geometry("900x600")
        self.style = ttk.Style()  # Initialize ttkbootstrap Style
        self.style.theme_use("superhero")  # Apply theme correctly ✅

        self.utils = Utils(root)
        self.camera = Camera(root, self.utils, self.show_user_info)  # ✅ Pass show_user_info as callback
        self.user_service = UserService()
        self.survey = Survey(root, self.utils, self.camera, self.ask_how_are_you)
        self.register = Register(root, self.utils)

        self.main_window()

    def main_window(self):
        """ Displays the main welcome screen. """
        self.utils.clear_window()
        self.utils.create_label("Welcome to Dr.Robot", 24, pady=20, weight="bold")
        
        # Use ttkbootstrap Button
        ttk.Button(self.root, text="Start", command=self.ask_new_user, bootstyle=SUCCESS).pack(pady=10)

    def ask_new_user(self):
        """ Ask if the user is new. """
        self.utils.clear_window()
        self.utils.create_label("Are you a new user?", 16, pady=20)

        button_frame = ttk.Frame(self.root)
        button_frame.pack()

        ttk.Button(button_frame, text="Yes", command=self.register.show_registration_form, bootstyle=PRIMARY).pack(side="left", padx=20)
        ttk.Button(button_frame, text="No", command=self.camera.start_camera, bootstyle=DANGER).pack(side="left", padx=20)

    def ask_how_are_you(self):
        """ Ask how the user is feeling today. """
        self.survey.ask_how_are_you()

    def show_user_info(self):
        print("✅ Transitioning to user info screen...")
        """ Displays user info after successful face recognition login. """
        self.utils.clear_window()  # ✅ Ensure the UI resets

        if APIService.user_data:
            user = APIService.user_data  # ✅ Retrieve stored user data

            self.utils.create_label(f"👤 Username: {user['name']}", 14)
            self.utils.create_label(f"📧 Email: {user['email']}", 14)
            self.utils.display_image("captured_images/captured_photo.jpg", 200, 200)
            self.utils.create_label(f"Welcome, {user['name']}!", 16, "bold")

            ttk.Button(self.root, text="Next", command=self.ask_how_are_you, bootstyle=INFO).pack(pady=10)
        else:
            self.utils.show_toast("Error", "User data not found! Please try again.")
# Run the app
root = ttk.Window(themename="superhero")  # Bootstrap window
app = DrRobotApp(root)
root.mainloop()

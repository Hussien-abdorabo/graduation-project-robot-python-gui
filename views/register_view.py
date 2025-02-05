# views/register_view.py
from tkinter import Entry, Label, Button

class RegisterView:
    def __init__(self, root, utils, controller, camera_view):
        self.root = root
        self.utils = utils
        self.controller = controller
        self.camera_view = camera_view  # ✅ Camera View for UI handling

        # ✅ Initialize entry fields
        self.name_entry = None
        self.email_entry = None
        self.password1_entry = None
        self.password2_entry = None
        self.image_path = None  # ✅ Store image path globally

    def show_registration_form(self, prefill_data=None):
        """ Displays the registration form """
        self.utils.clear_window()
        self.utils.create_label("📝 User Registration", 18, "bold")

        name_value = prefill_data.get("name", "") if prefill_data else ""
        email_value = prefill_data.get("email", "") if prefill_data else ""
        password1_value = prefill_data.get("password1", "") if prefill_data else ""
        password2_value = prefill_data.get("password2", "") if prefill_data else ""
        self.image_path = prefill_data.get("photo", "") if prefill_data else ""  # ✅ Get stored image
        print(self.image_path)

        Label(self.root, text="Full Name:").pack(pady=5)
        self.name_entry = Entry(self.root)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, name_value)

        Label(self.root, text="Email Address:").pack(pady=5)
        self.email_entry = Entry(self.root)
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, email_value)

        Label(self.root, text="Password:").pack(pady=5)
        self.password1_entry = Entry(self.root, show="*")
        self.password1_entry.pack(pady=5)
        self.password1_entry.insert(0, password1_value)

        Label(self.root, text="Confirm Password:").pack(pady=5)
        self.password2_entry = Entry(self.root, show="*")
        self.password2_entry.pack(pady=5)
        self.password2_entry.insert(0, password2_value)

        Button(self.root, text="📷 Capture Profile Photo", command=self.start_camera).pack(pady=10)

        # ✅ Show the captured image if available
        if self.image_path:
            self.utils.display_image(self.image_path, 200, 200)  # ✅ Display the saved image

        Button(self.root, text="Register", command=self.register_user).pack(pady=10)

    def start_camera(self):
        """ Saves user data and opens the camera for capturing profile photo. """
        if self.controller.save_user_data(
                self.name_entry.get(), self.email_entry.get(),
                self.password1_entry.get(), self.password2_entry.get()
        ):
            self.camera_view.show_camera_loading()  # ✅ Show loading first
            self.root.after(1000, self.camera_view.show_camera_feed)  # ✅ Open camera, but don't capture yet

    def capture_photo(self):
        """ Captures photo, stores it, and returns to registration form. """
        image_path = self.controller.camera_controller.capture_photo()  # ✅ Ensure it's stored correctly
        if image_path:
            self.image_path = image_path  # ✅ Store the image path globally
            self.controller.save_user_data(
                self.name_entry.get(), self.email_entry.get(),
                self.password1_entry.get(), self.password2_entry.get(),
                self.image_path  # ✅ Pass the capture function as a callback
            )
            prefill_data = self.controller.handle_registration_photo(image_path)  # ✅ Ensure correct storage
            self.show_registration_form(prefill_data=prefill_data)  # ✅ Reload form with image
        else:
            self.utils.show_toast("Error", "Failed to capture photo! Please try again.")

    def register_user(self):
        self.controller.save_user_data(
            self.name_entry.get(), self.email_entry.get(),
            self.password1_entry.get(), self.password2_entry.get(),
            self.image_path  # ✅ Pass the capture function as a callback
        )
        print(self.image_path)
        """ Triggers user registration """
        self.controller.register_user()

# views/doctor_view.py
from tkinter import Label, Button, Frame

class DoctorView:
    def __init__(self, root, utils, controller,app):
        self.root = root
        self.utils = utils
        self.controller = controller
        self.app = app

    def ask_user_to_continue(self):
        """ Ask the user if they want to continue speaking with the doctor. """
        self.utils.create_label("Would you like to continue speaking with the doctor?", 14, "bold")

        button_frame = Frame(self.root)
        button_frame.pack(pady=10)

        self.utils.create_button("Yes", self.show_qr_code, frame=button_frame, side="left", padx=20)
        self.utils.create_button("No", self.app.exit_application, frame=button_frame, side="left", padx=20)

    def goodbye_message(self):
        """ Displays a farewell message. """
        self.utils.clear_window()
        self.utils.create_label("✨ I wish you being better! ✨", 16, "bold")
        self.root.after(3000, self.root.quit)

    def show_qr_code(self):
        """ Displays a QR code for doctor consultation. """
        self.utils.clear_window()
        self.utils.create_label("📲 Scan this QR code to continue speaking with a doctor.", 14, "bold")

        qr_path = self.controller.get_qr_path()
        if qr_path:
            self.utils.display_image(qr_path, 300, 300)
        else:
            self.utils.create_label("🚨 QR Code not found!", 14, "bold")

        self.utils.create_button("Exit", self.app.exit_application)

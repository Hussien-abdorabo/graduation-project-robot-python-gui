import os
import tkinter as tk

class DoctorConsultation:
    def __init__(self, root, utils):
        self.root = root
        self.utils = utils
        self.QR_IMAGE_PATH = "QR.png"  # The QR code image

    def ask_user_to_continue(self):
        """ Ask the user if they want to continue speaking with the doctor. """
        # self.utils.clear_window()
        self.utils.create_label("Would you like to continue speaking with the doctor?", 14, "bold")

        # ✅ Create button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # ✅ Yes Button → Show QR Code
        self.utils.create_button("Yes", self.show_qr_code, 10, button_frame, "left", 20)

        # ✅ No Button → Show Farewell Message & Exit
        self.utils.create_button("No", self.goodbye_message, 10, button_frame, "left", 20)

    def goodbye_message(self):
        """ Displays a farewell message and exits the program. """
        self.utils.clear_window()
        self.utils.create_label("✨ I wish you being better! ✨", 16, "bold")
        self.utils.create_label("I was so happy to help you, and I'm here for any questions! 😊", 14)

        self.root.after(3000, self.root.quit)  # ✅ Exit after 3 seconds

    def show_qr_code(self):
        """ Displays a QR code to download the app and continue speaking with the doctor. """
        self.utils.clear_window()
        self.utils.create_label("📲 Scan this QR code to download the app and continue speaking with the doctor.", 14, "bold")

        # ✅ Show QR Code if available
        if os.path.exists(self.QR_IMAGE_PATH):
            self.utils.display_image(self.QR_IMAGE_PATH, 300, 300)
        else:
            self.utils.create_label("🚨 QR Code not found!", 14, "bold")

        # ✅ Exit Button Below QR Code
        self.utils.create_button("Exit", self.goodbye_message, 10)

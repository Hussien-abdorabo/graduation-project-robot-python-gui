import os
import tkinter as tk

class QRAssistant:
    def __init__(self, root, utils, next_step):
        self.root = root
        self.utils = utils
        self.next_step = next_step  # Function to proceed with image capture
        self.QR_IMAGE_PATH = "QR.png"  # ✅ QR code image path



    def show_qr_code_for_co_pilot(self):
        """ Displays a QR code and refers the user to Co-Pilot Assistant. """
        self.utils.clear_window()
        self.utils.create_label("📲 Please scan this QR code and refer to Co-Pilot Assistant.", 14, "bold")

        # ✅ Display QR Code if available
        if os.path.exists(self.QR_IMAGE_PATH):
            self.utils.display_image(self.QR_IMAGE_PATH, 300, 300)
        else:
            self.utils.create_label("🚨 QR Code not found!", 14, "bold")

        # ✅ Exit Button
        self.utils.create_button("Exit", self.exit_application, 10)

    def exit_application(self):
        """ Show exit message and close the application. """
        self.utils.clear_window()
        self.utils.create_label("✨ Thank you for using Dr. Robot! ✨", 16, "bold")
        self.utils.create_label("I am always here if you need any help! 😊", 14)
        self.root.after(3000, self.root.quit)  # ✅ Exit after 3 seconds

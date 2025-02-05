# views/qr_view.py
from tkinter import Label, Button

class QRView:
    def __init__(self, root, utils, controller):
        self.root = root
        self.utils = utils
        self.controller = controller

    def show_qr_code(self):
        """ Displays a QR code UI """
        self.utils.clear_window()
        self.utils.create_label("📲 Please scan this QR code.", 14, "bold")

        qr_path = self.controller.get_qr_path()
        if qr_path:
            self.utils.display_image(qr_path, 300, 300)
        else:
            self.utils.create_label("🚨 QR Code not found!", 14, "bold")

        self.utils.create_button("Exit", self.exit_application)

    def exit_application(self):
        """ Exits the application """
        self.utils.clear_window()
        self.utils.create_label("✨ Thank you for using Dr. Robot! ✨", 16, "bold")
        self.root.after(3000, self.root.quit)

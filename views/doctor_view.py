# views/doctor_view.py
from tkinter import Label, Button, Frame, ttk


class DoctorView:
    def __init__(self, root, utils, controller,app):
        self.root = root
        self.utils = utils
        self.controller = controller
        self.app = app

    def ask_user_to_continue(self):
        """ Ask the user if they want to continue speaking with the doctor. """
        # ✅ Create a frame for alignment (this ensures the label and buttons are closer together)
        container_frame = ttk.Frame(self.root)
        container_frame.pack(expand=True)  # Centers everything vertically

        # ✅ Label inside the container (pady reduced to keep it close to the buttons)
        label = ttk.Label(container_frame, text="Would you like to continue speaking with the doctor?", font=("Helvetica", 16))
        label.pack(pady=10)  # ✅ Reduce padding to keep it closer to buttons

        # ✅ Create a single frame for buttons (inside the same container)
        button_frame = ttk.Frame(container_frame)
        button_frame.pack(pady=60)  # ✅ Ensure buttons are just below the label

        # ✅ Create buttons inside button_frame to align in a row
        btn_yes = ttk.Button(button_frame, text="Good", command=self.show_qr_code, width=15,
                             bootstyle="success")
        btn_yes.pack(side="left", padx=10)

        btn_no = ttk.Button(button_frame, text="Bad", command=self.app.exit_application,
                            width=15, bootstyle="danger")
        btn_no.pack(side="left", padx=10)

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

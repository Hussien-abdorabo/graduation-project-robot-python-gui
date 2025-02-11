from tkinter import Label, Button, Frame
from PIL import Image, ImageTk
import os
from tkinter import Toplevel, Label


class Utils:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)  # ✅ Enable Fullscreen Mode by Default
        self.root.bind("<Escape>", self.exit_fullscreen)  # Press ESC to exit fullscreen

    def exit_fullscreen(self, event=None):
        """ Exit fullscreen when Escape key is pressed. """
        self.root.attributes('-fullscreen', False)

    def clear_window(self):
        """ Clears all widgets. """
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_label(self, text, font_size, weight="normal", pady=10):
        """ Creates a centered label. """
        frame = Frame(self.root)
        frame.pack(expand=True)  # ✅ Centering the label
        label = Label(frame, text=text, font=("Helvetica", font_size, weight))
        label.pack(pady=pady)

    def create_button(self, text, command, width=10, frame=None, side="top", padx=0):
        """ Creates a centered button inside the specified frame. """
        parent = frame if frame else self.root

        button_frame = Frame(parent)  # ✅ Center the button
        button_frame.pack(expand=True)
        btn = Button(button_frame, text=text, command=command, width=width)
        btn.pack(side=side, padx=padx, pady=5)

    def display_image(self, image_path, width, height):
        """ Displays a centered image in the UI. """
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((width, height))
            img = ImageTk.PhotoImage(img)

            img_frame = Frame(self.root)  # ✅ Center image
            img_frame.pack(expand=True)
            img_label = Label(img_frame, image=img)
            img_label.image = img
            img_label.pack()
        else:
            self.create_label("Image not found", 14, "bold")

    def show_toast(self, message_type="info", message="", duration=3000):
        """ Displays a temporary toast notification with different styles. """
        toast = Toplevel(self.root)
        toast.overrideredirect(True)
        toast.geometry("+500+300")

        # 🎨 Set colors based on message type
        if message_type == "Error":
            bg_color = "red"
            icon = "❌ "
        elif message_type == "Warning":
            bg_color = "orange"
            icon = "⚠️ "
        else:  # Default to "info"
            bg_color = "green"
            icon = "✅ "

        Label(toast, text=f"{icon} {message}", bg=bg_color, fg="white", font=("Arial", 12)).pack(padx=10, pady=5)
        self.root.after(duration, toast.destroy)

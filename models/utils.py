from PIL import Image, ImageTk, ImageDraw
import os
from tkinter import Toplevel, Label
from ttkbootstrap import Frame, Button  # ✅ Correct usage


class Utils:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)  # ✅ Enable Fullscreen Mode by Default
        self.root.bind("<Escape>", self.exit_fullscreen)  # Press ESC to exit fullscreen
    def speak_arabic(text,languge='en'):
        print(text)
        # audio_file = f"audio-{uuid.uuid4()}.mp3"
        # tts = gTTS(text=text,lang="en")
        # tts.save(audio_file)
        # playsound(audio_file)
        #
        # # Clean up
        # os.remove(audio_file)
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
        # ✅ Ensure speech happens every time a new label appears

    def create_button(self, text, command, width=10, frame=None, side="top", padx=0, bootstyle="info"):
        """ Creates a rounded button using ttkbootstrap. """
        parent = frame if frame else self.root

        button_frame = Frame(parent)  # ✅ Ensure this is ttkbootstrap.Frame
        button_frame.pack(expand=True)

        btn = Button(
            button_frame,
            text=text,
            command=command,
            width=width,
            bootstyle=bootstyle  # ✅ Use a valid bootstyle
        )
        btn.pack(side=side, padx=padx, pady=5)

    def display_image(self, image_path, width, height):
        """ Displays a centered rounded image in the UI. """
        if os.path.exists(image_path):
            img = Image.open(image_path).resize((width, height), Image.LANCZOS)
            img = img.convert("RGBA")  # ✅ Ensure transparency support

            # ✅ Create a circular mask
            mask = Image.new("L", (width, height), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, width, height), fill=255)

            # ✅ Apply the mask to round the corners
            img.putalpha(mask)

            # ✅ Convert for Tkinter display
            img = ImageTk.PhotoImage(img)

            img_frame = Frame(self.root)  # ✅ Center image
            img_frame.pack(expand=True, pady=10)
            img_label = Label(img_frame, image=img, borderwidth=0)
            img_label.image = img
            img_label.pack()
        else:
            self.create_label("Image not found", 16, "bold")

    def show_toast(self, message_type="info", message="", duration=5000):
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

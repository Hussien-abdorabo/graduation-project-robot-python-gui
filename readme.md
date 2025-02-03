# 🏥 Dr. Robot - Skin Disease Diagnosis System

## 📌 Project Overview
Dr. Robot is an AI-powered **skin disease diagnosis system** designed to assist users in identifying potential skin diseases and consulting with doctors. The system provides:
- 📸 **Photo-based diagnosis**
- 📝 **User registration with profile photos**
- 🔍 **AI-based disease detection (placeholder for AI model integration)**
- 📲 **QR-based consultation with doctors**

This project is built using **Python (Tkinter GUI)** and follows a modular structure for easy scalability and maintenance.

---

## 🌟 Features
- ✅ **User Registration**: Users register with their **name, email, password, and profile photo**.
- ✅ **Profile Photo Capture**: Users take a photo using their webcam, which is stored and linked to their account.
- ✅ **Skin Disease Assessment**: Users can upload a skin disease image for analysis.
- ✅ **Doctor Consultation**: Users can scan a QR code to proceed with doctor consultation.
- ✅ **Modular Structure**: Each major component (registration, camera, consultation) is implemented as a separate module.
- ✅ **Full-Screen UI**: The application starts in full-screen mode for better usability.
- ✅ **Error Handling**: Includes user-friendly validation and error messages.

---

## 🛠 Installation Guide

### 1️⃣ **System Requirements**
- Python 3.10 or later
- Windows/Linux/macOS
- Webcam for profile photo capture

### 2️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-repo/dr-robot.git
cd dr-robot
```

### 3️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

### 4️⃣ **Run the Application**
```sh
python index.py
```

The application will launch in **full-screen mode**.

---

## 🎮 Usage Guide

### 📝 **User Registration**
1. On launch, you will be asked if you are a new user.
2. Click **"Yes"** to open the **registration form**.
3. Enter your **name, email, password**, and **confirm your password**.
4. Click **"Capture Profile Photo"** to take a picture with your webcam.
5. Click **"Register"** to save your details.

### 🔬 **Skin Disease Diagnosis**
1. After registering, you will be asked if you can provide an image of your disease.
2. If **"Yes"**, capture or upload the image.
3. If **"No"**, you will be redirected to scan a QR code for **doctor consultation**.

### 📲 **Doctor Consultation via QR Code**
1. If you prefer consulting a doctor directly, scan the **QR code** displayed on the screen.
2. Follow the instructions in the app linked via the QR code.

### 🚀 **Exiting the App**
- Press **ESC** to exit full-screen mode.
- Click **Exit** on any screen to close the application.

---

## 📂 Project Structure
```
📦 dr-robot
 ┣ 📂 assets                # UI assets (icons, QR codes)
 ┣ 📂 captured_images       # Temporary photo storage before saving
 ┣ 📂 user_photos          # User profile pictures (saved permanently)
 ┣ 📜 index.py             # Main entry point
 ┣ 📜 register.py          # User registration module
 ┣ 📜 camera.py            # Webcam photo capture
 ┣ 📜 survey.py            # Disease survey module
 ┣ 📜 qr_assistant.py      # QR code module for doctor consultation
 ┣ 📜 doctor_consultation.py # Doctor recommendation system
 ┣ 📜 utils.py             # UI helper functions
 ┗ 📜 requirements.txt     # Required dependencies
```

---

## 🚀 Future Enhancements
🔹 **AI Model Integration**: Use a machine learning model for real skin disease prediction.
🔹 **Database Storage**: Save user data in SQLite/MySQL instead of local files.
🔹 **API Integration**: Connect with an online doctor consultation platform.
🔹 **Multilingual Support**: Support additional languages for wider accessibility.

---

## 🤝 Contributing
If you want to contribute:
1. Fork the repository.
2. Create a feature branch (`feature-xyz`).
3. Commit your changes.
4. Create a Pull Request.

---

## 📜 License
This project is licensed under the **MIT License**. Feel free to use and modify it for your needs.

**👨‍⚕️ Dr. Robot - Your AI Assistant for Skin Disease Diagnosis!** 🚀


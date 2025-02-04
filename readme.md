# Dr. Robot - Skin Disease Diagnosis

Dr. Robot is a GUI-based skin disease diagnosis assistant that leverages AI-powered analysis to detect potential skin diseases. The application allows users to capture images of their skin conditions and provides medical recommendations, including doctor details for further consultation.

## Features
- **User Authentication**: Login and register using facial recognition.
- **AI Diagnosis**: Upload or capture an image of the skin condition for AI-based analysis.
- **Doctor Consultation**: Get recommendations on doctors based on AI results.
- **QR Assistant**: Scan QR codes for additional assistance.
- **Interactive UI**: Built with `tkinter` and `ttkbootstrap` for an intuitive user experience.

## Technologies Used
- **Python** (Tkinter for UI)
- **OpenCV** (for image capture and processing)
- **PIL (Pillow)** (for image handling)
- **Requests** (for API communication)
- **TTK Bootstrap** (for enhanced UI styling)

## Installation
### Prerequisites
Ensure you have Python 3.10+ installed on your system.

### Setup Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/dr-robot.git
   cd dr-robot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the `.env` file with the API base URL:
   ```plaintext
   BASE_URL=<your_api_base_url>
   ```

## Running the Application
Execute the following command:
```bash
python main.py
```

## Project Structure
```
📂 dr-robot
│-- main.py              # Main entry point for the application
│-- survey.py            # Handles user survey for skin condition evaluation
│-- camera.py            # Handles image capture functionality
│-- utils.py             # Utility functions for UI components
│-- user_service.py      # Simulated user data
│-- api_service.py       # API calls for login, registration, and diagnosis
│-- doctor_consultation.py # Handles doctor consultation options
│-- qr_assistant.py      # QR code functionality
│-- register.py          # User registration logic
│-- requirements.txt     # Dependencies list
│-- .env                 # Environment variables (API keys, etc.)
```

## Usage
1. **Login / Register**:
   - If new, register with name, email, password, and profile photo.
   - If existing, log in using facial recognition.

2. **Survey and Diagnosis**:
   - Answer simple questions about skin conditions.
   - Capture an image of the affected area.
   - Wait for AI diagnosis results.

3. **Doctor Consultation**:
   - Based on AI analysis, receive doctor recommendations.
   - View doctor details including name, contact, and location.

4. **QR Assistant**:
   - Scan a QR code for additional support or to download an app.

## Known Issues & Future Improvements
- Enhance AI model accuracy with more datasets.
- Improve UI responsiveness for smaller screens.
- Add multilingual support.

## Contributors
- **Abdalrhman Alkady** - Team Leader / Developer
- **Ahmed Mahmoud** - Developer / AI Specialist
- **Ziad Ahmed** - App Developer
- **ElHussien Ali** - Backend Developer
- **Assem Ragab** - Frontend Developer
- **Anas Ahmed** - Frontend Developer

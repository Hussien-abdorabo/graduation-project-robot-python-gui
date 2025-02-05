# controllers/survey_controller.py
import os
from models.api_service import APIService

class SurveyController:
    def __init__(self, camera_controller):
        self.camera_controller = camera_controller
        self.DISEASE_IMAGE_DIR = "assets/diseases-photos"
        os.makedirs(self.DISEASE_IMAGE_DIR, exist_ok=True)

    def start_scan_process(self):
        """ Starts the scanning process """
        if not self.camera_controller.start_camera():
            print("❌ Camera failed to start")
            return False
        return True

    def capture_and_store(self):
        """ Captures the photo and stores it before diagnosis """
        image_path = os.path.join(self.DISEASE_IMAGE_DIR, "disease_photo.jpg")

        # ✅ Ensure the camera is open before capturing
        if not self.camera_controller.start_camera():
            print("❌ Camera not open, cannot capture image")
            return None

        filename = self.camera_controller.capture_photo(image_path)  # ✅ Pass correct argument

        if filename and os.path.exists(filename):
            print(f"✅ Image captured successfully: {filename}")
            return filename
        else:
            print("❌ Image capture failed!")
            return None
    def diagnose_skin_disease(self, image_path):
        """ Sends the captured image for diagnosis """
        if not os.path.exists(image_path):
            return {"status": "error", "message": "Image not found"}

        response = APIService.diagnose_skin_disease(image_path)
        return response

    def get_doctor_data(self):
        """ Fetches doctor details from APIService. """
        return APIService.user_data.get("doctor", {})


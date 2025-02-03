import requests
import os
import json
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()
BASE_URL = os.getenv("BASE_URL")

class APIService:
    token = None  # ✅ Store token globally

    @staticmethod
    def register_user(name, email, password, image_path):
        """ Sends user registration data to the backend API and saves the token. """
        url = f"{BASE_URL}/register"
        files = {'photo': open(image_path, 'rb')}
        data = {'name': name, 'email': email, 'password': password}

        try:
            response = requests.post(url, data=data, files=files)
            result = response.json()

            if result.get("success"):
                APIService.token = result.get("token")  # ✅ Save token globally
                return {"success": True, "message": "Registration successful!", "token": APIService.token}
            else:
                return {"success": False, "message": result.get("message", "Registration failed.")}

        except requests.exceptions.RequestException as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def diagnose_skin_disease(image_path):
        """ Sends a captured image to the backend AI model for skin disease diagnosis. """
        url = f"{BASE_URL}/diagnose"
        files = {'image': open(image_path, 'rb')}
        headers = {}

        if APIService.token:
            headers["Content-Type"] = "multipart/form-data"
            headers["Accept"] = "application/json"
            headers["Authorization"] = f"Bearer {APIService.token}"  # ✅ Include token in request

        try:
            response = requests.post(url, headers=headers, files=files)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": str(e)}

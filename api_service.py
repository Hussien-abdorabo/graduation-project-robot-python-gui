import requests
import json

class APIService:
    BASE_URL = "http://localhost:5000/api"  # Change this to your actual backend URL

    @staticmethod
    def register_user(name, email, password, image_path):
        """ Sends user registration data to the backend API. """
        url = f"{APIService.BASE_URL}/register"
        files = {'profile_photo': open(image_path, 'rb')}
        data = {'name': name, 'email': email, 'password': password}

        try:
            response = requests.post(url, data=data, files=files)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def diagnose_skin_disease(image_path):
        """ Sends a captured image to the backend AI model for skin disease diagnosis. """
        url = f"{APIService.BASE_URL}/diagnose"
        files = {'image': open(image_path, 'rb')}

        try:
            response = requests.post(url, files=files)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": str(e)}

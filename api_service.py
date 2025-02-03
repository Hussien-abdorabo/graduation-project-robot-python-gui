import requests
import os
import json
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()
BASE_URL = os.getenv("BASE_URL")

class APIService:
    token = None  # ✅ Store token globally
    user_data = None  # ✅ Store user info globally

    @staticmethod
    def login_with_face(image_path):
        """ Sends the captured face photo to the backend for login via face recognition. """
        url = f"{BASE_URL}/login"
        files = {'photo': open(image_path, 'rb')}

        try:
            print(f"🔍 Sending face photo for login: {image_path}")
            response = requests.post(url, files=files)
            print(f"🔍 Response Status Code: {response.status_code}")
            print(f"🔍 Response Content: {response.text}")  # ✅ Print full response

            result = response.json()
            print(f"🔍 Parsed JSON Response: {result}")  # ✅ Debug full JSON response

            # ✅ Check if 'token' exists in the response
            if "token" in result:
                print(f"✅ Token found: {result['token']}")  # ✅ Debug: Show extracted token
            else:
                print("❌ Token NOT found in the response!")

            # ✅ Check if 'user' exists in the response
            if "user" in result:
                print(f"✅ User info found: {result['user']}")
            else:
                print("❌ User info NOT found in the response!")

            # ✅ Only proceed if both token and user exist
            if "token" in result and "user" in result:
                APIService.token = result["token"]  # ✅ Save token globally
                APIService.user_data = result["user"]  # ✅ Store user info
                return {"success": True, "message": "Login successful!", "user": APIService.user_data,
                        "token": APIService.token}
            else:
                return {"success": False, "message": "Token or user data missing in API response."}

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Request Error: {str(e)}")
            return {"success": False, "message": str(e)}

    @staticmethod
    def register_user(name, email, password,password_confirmation,type, image_path):
        """ Sends user registration data to the backend API and saves the token. """
        url = f"{BASE_URL}/register"
        files = {'photo': open(image_path, 'rb')}
        data = {'name': name, 'email': email, 'password': password, 'password_confirmation': password_confirmation,'type':type}

        try:
            response = requests.post(url, data=data, files=files)
            print(f"🔍 Registration Response: {response.text}")
            result = response.json()
            print(f"🔍 Registration Response: {result}")

            if "token" in result and "user" in result:
                APIService.token = result.get("token")  # ✅ Save token globally
                APIService.user_data = result.get("user")  # ✅ Store user info
                return {"success": True, "message": "Registration successful!", "token": APIService.token, "user": APIService.user_data}
            else:
                return {"success": False, "message": result.get("message", "Registration failed.")}

        except requests.exceptions.RequestException as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def diagnose_skin_disease(image_path):
        """ Sends a captured image to the backend AI model for skin disease diagnosis. """
        url = f"{BASE_URL}/robot/diagnose"

        headers = {
            "Authorization": f"Bearer {APIService.token}",  # ✅ Ensure token is included
        }

        try:
            print(f"🔍 Sending image for diagnosis: {image_path}")

            # ✅ Use correct multipart encoding
            with open(image_path, 'rb') as image_file:
                files = {'image': ('disease_photo.jpg', image_file, 'image/jpeg')}
                response = requests.post(url, headers=headers, files=files)

            print(f"🔍 Response Status Code: {response.status_code}")
            print(f"🔍 Response Content: {response.text}")

            return response.json()  # ✅ Parse JSON response

        except json.JSONDecodeError:
            print("⚠️ JSON Decode Error - API response is not valid JSON")
            return {"success": False, "message": "Invalid JSON response from API"}

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Request Error: {str(e)}")
            return {"success": False, "message": str(e)}


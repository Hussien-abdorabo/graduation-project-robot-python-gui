import os


class DoctorController:
    def __init__(self, utils):
        self.utils = utils
        self.QR_IMAGE_PATH = "assets/QR.png"

    def get_qr_path(self):
        """ Returns the path of the QR image """
        return self.QR_IMAGE_PATH if os.path.exists(self.QR_IMAGE_PATH) else None

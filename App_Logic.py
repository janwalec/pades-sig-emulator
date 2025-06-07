import os
from encryption_manager import *

class AppLogic:
    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.file_chosen = None
        self.pendrive_attached = ""
        self.key_found = None
        self.full_path = ""

    def check_if_pdf(self, file_name):
        return file_name.lower().endswith(".pdf")

    def detect_key(self):
        if self.pendrive_attached == "":
            return False

        output_path = os.path.join("keys_bsk", "private_key.enc")
        full_path = os.path.join(self.pendrive_attached, output_path)
        self.full_path = full_path
        try:
            with open(full_path, "rb") as f:
                self.key_found = True
                return True
        except FileNotFoundError:
            self.key_found = False
            return False

    def set_pendrive(self, pendrive):
        self.pendrive_attached = pendrive

    def set_file(self, filename):
        if filename and self.check_if_pdf(filename):
            self.file_chosen = filename
            return True
        else:
            self.file_chosen = None
            return False

    def generate_key(self, pin):
        private_key, public_key = self.encryption_manager.generate_RSA_keys()
        encrypted = self.encryption_manager.AES_key_encryption(pin, private_key)
        with open(self.full_path, "wb") as f:
            f.write(encrypted)
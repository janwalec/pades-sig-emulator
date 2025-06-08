import os
#from Crypto.SelfTest.Protocol.test_ecdh import public_key
from Crypto.Signature import pkcs1_15

from encryption_manager import *

class AppLogic:
    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.file_chosen = None
        self.pendrive_attached = ""
        self.encrypted_key_on_pendrive = None
        self.full_path = ""
        self.path_to_public_keys = os.path.join("stored_public_keys", "key.pub")
        self.decrypted_key = None
        self.pdf_to_sign = None

    def check_if_pdf(self, file_name):
        return file_name.lower().endswith(".pdf")

    def detect_key(self):
        # searches for private, encrypted key on attached device
        if self.pendrive_attached == "":
            return False

        output_path = os.path.join("keys_bsk", "private_key.enc")
        full_path = os.path.join(self.pendrive_attached, output_path)
        self.full_path = full_path
        try:
            with open(full_path, "rb") as f:
                self.encrypted_key_on_pendrive = f.read()
                return True
        except FileNotFoundError:
            self.encrypted_key_on_pendrive = None
            return False

    def set_pendrive(self, pendrive):
        self.pendrive_attached = pendrive

    def set_file(self, filename):
        # method that saves PATH to pdf file
        if filename and self.check_if_pdf(filename):
            # filename is not empty and it is *.pdf
            self.file_chosen = filename
            return True
        else:
            # filename empty or file chosen is not *.pdf
            self.file_chosen = None
            return False

    def save_keys(self, public_key, encrypted_key):
        # saves encrypted key on user's removable device, and public key on hard drive
        with open(self.full_path, "wb") as f:
            f.write(encrypted_key)

        with open(self.path_to_public_keys, "wb") as f:
            f.write(public_key)

    def generate_key(self, pin):
        # generates private key based on pin
        private_key, public_key = self.encryption_manager.generate_RSA_keys()
        encrypted = self.encryption_manager.AES_key_encryption(pin, private_key)
        self.save_keys(public_key, encrypted)

    def compare_pin(self, pin):
        # decrypts encrypted private key with pin and checks for errors
        with open(self.path_to_public_keys, "rb") as f:
            try:
                print(self.encrypted_key_on_pendrive)
                self.decrypted_key = self.encryption_manager.decrypt_private_key(self.encrypted_key_on_pendrive, pin)
            except ValueError as e:
                self.decrypted_key = None
                raise e

    def sign_document(self):
        # hashes chosen pdf and signs the hash, then saves it on hard drive
        if self.decrypted_key is None:
            raise ValueError("Private key missing")

        if not self.pdf_to_sign:
            raise ValueError("Wrong pdf")

        private_key = RSA.import_key(self.decrypted_key)

        pdf_hash = self.encryption_manager.hash_pdf(self.pdf_to_sign)

        signature = pkcs1_15.new(private_key).sign(pdf_hash)

        signature_path = os.path.join("pdf", "signed_signature.sig")
        with open(signature_path, "wb") as f:
            f.write(signature)

    def check_signed_document(self):
        # checks if signed hash is associated with public key saved on hard drive
        if not self.pdf_to_sign:
            raise ValueError("Wrong pdf")
        public_key_file = None
        with open(self.path_to_public_keys, "rb") as f:
            public_key_file = f.read()

        public_key = RSA.import_key(public_key_file)
        pdf_hash = self.encryption_manager.hash_pdf(self.pdf_to_sign)

        signature_path = os.path.join("pdf", "signed_signature.sig")
        signature = None
        with open(signature_path, "rb") as f:
            signature = f.read()
        try:
            pkcs1_15.new(public_key).verify(pdf_hash, signature)
            return True
        except ValueError as e:
            return False



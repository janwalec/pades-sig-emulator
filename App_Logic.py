import os
from Crypto.Signature import pkcs1_15
from encryption_manager import *

##
# @brief Klasa logiki aplikacji, obsługująca operacje na kluczach i podpisywaniu dokumentów PDF
class AppLogic:
    ##
    # @brief Konstruktor klasy inicjalizujący menedżera szyfrowania oraz zmienne stanu
    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.file_chosen = None
        self.pendrive_attached = ""
        self.encrypted_key_on_pendrive = None
        self.full_path = ""
        self.path_to_public_keys = os.path.join("stored_public_keys", "key.pub")
        self.decrypted_key = None
        self.pdf_to_sign = None

    ##
    # @brief Sprawdza czy podany plik to PDF
    # @param file_name Nazwa pliku do sprawdzenia
    # @return bool True jeśli plik ma rozszerzenie .pdf, False w przeciwnym razie
    def check_if_pdf(self, file_name):
        return file_name.lower().endswith(".pdf")

    ##
    # @brief Wykrywa zaszyfrowany klucz prywatny na dołączonym pendrive
    # @return bool True jeśli klucz został znaleziony, False w przeciwnym wypadku
    def detect_key(self):
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

    ##
    # @brief Ustawia ścieżkę do aktualnie podłączonego pendrive
    # @param pendrive Ścieżka do pendrive
    def set_pendrive(self, pendrive):
        self.pendrive_attached = pendrive

    ##
    # @brief Ustawia ścieżkę do wybranego pliku PDF do podpisania
    # @param filename Ścieżka do pliku
    # @return bool True jeśli plik jest poprawnym PDF, False jeśli nie
    def set_file(self, filename):
        if filename and self.check_if_pdf(filename):
            self.file_chosen = filename
            return True
        else:
            self.file_chosen = None
            return False

    ##
    # @brief Zapisuje klucze publiczny (na dysku) i zaszyfrowany klucz prywatny (na pendrive)
    # @param public_key Klucz publiczny w formacie bajtowym
    # @param encrypted_key Zaszyfrowany klucz prywatny w formacie bajtowym
    def save_keys(self, public_key, encrypted_key):
        with open(self.full_path, "wb") as f:
            f.write(encrypted_key)

        with open(self.path_to_public_keys, "wb") as f:
            f.write(public_key)

    ##
    # @brief Generuje parę kluczy RSA i szyfruje klucz prywatny na podstawie PIN-u
    # @param pin PIN używany do szyfrowania klucza prywatnego
    def generate_key(self, pin):
        private_key, public_key = self.encryption_manager.generate_RSA_keys()
        encrypted = self.encryption_manager.AES_key_encryption(pin, private_key)
        self.save_keys(public_key, encrypted)

    ##
    # @brief Próbuje "odszyfrować" zaszyfrowany klucz prywatny używając PIN. Sprawdza czy istnieje zapisany klucz publiczny.
    # @param pin PIN używany do odszyfrowania klucza prywatnego
    # @throws ValueError jeśli odszyfrowanie nie powiedzie się
    def compare_pin(self, pin):
        with open(self.path_to_public_keys, "rb") as f:
            try:
                self.decrypted_key = self.encryption_manager.decrypt_private_key(self.encrypted_key_on_pendrive, pin)
            except ValueError as e:
                self.decrypted_key = None
                raise e

    ##
    # @brief Podpisuje wybrany plik PDF używając klucza prywatnego
    # @throws ValueError jeśli klucz prywatny jest niezaładowany lub plik PDF nie został wybrany
    def sign_document(self):
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

    ##
    # @brief Weryfikuje podpis pliku PDF względem zapisanego klucza publicznego
    # @return bool True jeśli podpis jest poprawny, False w przeciwnym wypadku
    # @throws ValueError jeśli plik PDF nie został wybrany
    def check_signed_document(self):
        if not self.pdf_to_sign:
            raise ValueError("Wrong pdf")

        with open(self.path_to_public_keys, "rb") as f:
            public_key_file = f.read()

        public_key = RSA.import_key(public_key_file)
        pdf_hash = self.encryption_manager.hash_pdf(self.pdf_to_sign)

        signature_path = os.path.join("pdf", "signed_signature.sig")
        with open(signature_path, "rb") as f:
            signature = f.read()

        try:
            pkcs1_15.new(public_key).verify(pdf_hash, signature)
            return True
        except ValueError:
            return False

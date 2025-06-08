import os
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

##
# @brief Klasa zarządzająca szyfrowaniem, generowaniem kluczy RSA oraz szyfrowaniem AES
class EncryptionManager():
    ##
    # @brief Haszuje plik PDF używając SHA-256
    # @param file_path Ścieżka do pliku PDF
    # @return SHA256.Hash Obiekt z hashem pliku
    @staticmethod
    def hash_pdf(file_path):
        h = SHA256.new()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h

    ##
    # @brief Generuje parę kluczy RSA (prywatny i publiczny)
    # @return tuple Zwraca krotkę (private_key, public_key) w formacie bajtowym
    @staticmethod
    def generate_RSA_keys():
        print("GENERATING RSA")
        key = RSA.generate(4096)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        print("Generating finished")
        return private_key, public_key

    ##
    # @brief Szyfruje klucz prywatny AESem na podstawie PINu
    # @param pin PIN używany do utworzenia klucza AES
    # @param private_key Klucz prywatny RSA w formacie bajtowym
    # @return bytes Zaszyfrowany klucz prywatny wraz z IV
    @staticmethod
    def AES_key_encryption(pin, private_key):
        hasher = SHA256.new()
        hasher.update(pin.encode('utf-8'))
        aes_key = hasher.digest()

        cipher = AES.new(aes_key, AES.MODE_CBC)
        iv = cipher.iv

        padding_len = AES.block_size - len(private_key) % AES.block_size
        padded_key = private_key + bytes([padding_len]) * padding_len
        encrypted_key = cipher.encrypt(padded_key)

        return iv + encrypted_key

    ##
    # @brief Odszyfrowuje zaszyfrowany klucz prywatny AESem za pomocą PINu
    # @param encrypted_data Zaszyfrowany klucz prywatny (IV + ciphertext)
    # @param pin PIN do odszyfrowania klucza
    # @return bytes Odszyfrowany klucz prywatny RSA
    # @throws ValueError Jeśli padding jest nieprawidłowy (błędny PIN)
    @staticmethod
    def decrypt_private_key(encrypted_data: bytes, pin) -> bytes:
        iv = encrypted_data[:AES.block_size]
        ciphertext = encrypted_data[AES.block_size:]

        hasher = SHA256.new()
        hasher.update(pin.encode('utf-8'))
        aes_key = hasher.digest()

        cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
        padded_private_key = cipher.decrypt(ciphertext)

        padding_len = padded_private_key[-1]
        if padding_len < 1 or padding_len > AES.block_size:
            raise ValueError("Invalid padding. Wrong PIN")
        private_key = padded_private_key[:-padding_len]

        return private_key

    ##
    # @brief Konstruktor klasy (obecnie pusty)
    def __init__(self):
        pass

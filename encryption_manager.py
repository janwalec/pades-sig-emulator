import os
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import AES



class EncryptionManager():
    @staticmethod
    def generate_RSA_keys():
        key = RSA.generate(2056)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key

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


    def __init__(self):
        pass

'''
em = EncryptionManager()
pin = input("Enter PIN: ")
print("GENERATING RSA KEYS...")
private_key, public_key = em.generate_RSA_keys()
print(private_key, "\n", public_key)

print("ENCRYTING PRIVATE KEY...")
encrypted = em.AES_key_encryption(pin, private_key)
print(encrypted)

print("***********************************")
print("DECRYPTING ENCRYPTED PRIVATE KEY...")
pin = input("Enter PIN: ")
decrypted = em.decrypt_private_key(encrypted, pin)
print(decrypted)
'''
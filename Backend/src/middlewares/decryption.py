from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import os
from dotenv import load_dotenv

load_dotenv()

class DecryptionMiddleware:
    @staticmethod
    def decrypt(encrypted_data: dict):
        encryption_key = os.getenv("ENCRYPTION_KEY")

        if not encryption_key:
            raise ValueError("Missing encryption key in environment variables.")
        
        encryption_key = base64.b64decode(encryption_key)  

        if len(encryption_key) != 32:
            raise ValueError("Invalid encryption key length. Must be a 32-byte key.")

        decrypted_data = {}
        for key, value in encrypted_data.items():
            try:
                encrypted_bytes = base64.b64decode(value)
                iv, ciphertext = encrypted_bytes[:16], encrypted_bytes[16:]

                cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
                decrypted_data[key] = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

            except Exception as e:
                print(f"Decryption failed for key {key}: {str(e)}")
                decrypted_data[key] = None  

        return decrypted_data

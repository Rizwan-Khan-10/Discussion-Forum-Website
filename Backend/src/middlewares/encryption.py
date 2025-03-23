from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import os
from dotenv import load_dotenv

load_dotenv()

class EncryptionMiddleware:
    @staticmethod
    def encrypt(data: dict):
        encryption_key = os.getenv("ENCRYPTION_KEY")
        
        if not encryption_key:
            raise ValueError("Missing encryption key in environment variables.")
        
        encryption_key = base64.b64decode(encryption_key)  
        
        if len(encryption_key) != 32:
            raise ValueError("Invalid encryption key length. Must be a 32-byte key.")

        encrypted_data = {}
        for key, value in data.items():
            iv = os.urandom(16)
            cipher = AES.new(encryption_key, AES.MODE_CBC, iv)

            if isinstance(value, bytes):
                value = value.decode('utf-8', errors='ignore')  
            value = str(value)  

            encrypted_bytes = cipher.encrypt(pad(value.encode('utf-8'), AES.block_size))
            encrypted_text = base64.b64encode(iv + encrypted_bytes).decode()

            encrypted_data[key] = encrypted_text

        return encrypted_data

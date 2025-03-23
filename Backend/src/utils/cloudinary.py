import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_file(file_path, public_id=None):
    try:
        upload_result = cloudinary.uploader.upload(file_path, public_id=public_id)
        return upload_result.get('secure_url', ''), upload_result.get('public_id', '')  
    except Exception:
        return None, None

def retrieve_file(public_id):
    try:
        return cloudinary.utils.cloudinary_url(public_id, secure=True)[0]  
    except Exception:
        return None

def delete_file(public_id):
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception:
        pass

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

        cloud_name = cloudinary.config().cloud_name
        file_format = upload_result.get('format', 'jpg') 

        clean_url = f"https://res.cloudinary.com/{cloud_name}/image/upload/{public_id}.{file_format}"

        return clean_url, upload_result.get('public_id', '')  
    except Exception:
        return None, None

def delete_file(public_id):
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception:
        pass

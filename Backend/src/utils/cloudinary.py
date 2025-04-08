import cloudinary
import cloudinary.uploader
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
        if not file_path:
            print("File path is missing.")
            return None, None

        upload_result = cloudinary.uploader.upload(
            file_path,
            public_id=public_id,
            invalidate=True
        )

        if not upload_result:
            print("Upload failed. No result returned.")
            return None, None

        cloud_name = cloudinary.config().cloud_name
        file_format = upload_result.get('format', 'jpg')
        version = upload_result.get('version')

        if not public_id or not version:
            print("Missing public_id or version.")
            return None, None

        clean_url = f"https://res.cloudinary.com/{cloud_name}/image/upload/v{version}/{public_id}.{file_format}"

        return clean_url, upload_result.get('public_id', '')
    except Exception as e:
        print("Upload error:", e)
        return None, None

def delete_file(public_id):
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception:
        pass

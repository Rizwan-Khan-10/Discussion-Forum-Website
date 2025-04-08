from sqlalchemy.orm import Session
from models.userProfile import UserProfile
from models.user import User
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from pydantic import BaseModel
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
from typing import Optional
from fastapi import UploadFile
from utils.cloudinary import upload_file, delete_file
import os

class UserProfileRequest(BaseModel):
    bio: str 
    img: str 
    username: str
    blockUser: bool = False
    blockCommunity: bool = False
    blockPost: bool = False

async def get_user_profile(user_id: str, db: Session):
    try:
        matched_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

        if not matched_profile:
            raise APIError(status_code=404, detail="User profile not found.")

        decrypted_data = DecryptionMiddleware.decrypt({
            "bio": matched_profile.bio,
            "img": matched_profile.img,
            "blockUser": matched_profile.blockUser,
            "blockCommunity": matched_profile.blockCommunity,
            "blockPost": matched_profile.blockPost,
            "followers": matched_profile.followers,
            "following": matched_profile.following,
            "total_posts": matched_profile.total_posts,
            "total_upvotes": matched_profile.total_upvotes,
            "total_downvotes": matched_profile.total_downvotes,
            "reputation": matched_profile.reputation,
            "total_bookmarks": matched_profile.total_bookmarks,
            "total_shares": matched_profile.total_shares,
            "total_views": matched_profile.total_views,
        })

        response_data = {
            "user_id": user_id,
            "bio": decrypted_data.get("bio"),
            "img": decrypted_data.get("img"),
            "blockUser": decrypted_data.get("blockUser"),
            "blockCommunity": decrypted_data.get("blockCommunity"),
            "blockPost": decrypted_data.get("blockPost"),
            "followers": decrypted_data.get("followers"),
            "following": decrypted_data.get("following"),
            "total_posts": decrypted_data.get("total_posts"),
            "total_upvotes": decrypted_data.get("total_upvotes"),
            "total_downvotes": decrypted_data.get("total_downvotes"),
            "reputation": decrypted_data.get("reputation"),
            "total_bookmarks": decrypted_data.get("total_bookmarks"),
            "total_shares": decrypted_data.get("total_shares"),
            "total_views": decrypted_data.get("total_views"),
        }

        return APIResponse.success(data=response_data, message="User profile retrieved successfully.")

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def update_user_profile(user_id: str, username: str, bio: Optional[str], profilePic: Optional[UploadFile], db: Session):
    try:
        matched_user = db.query(User).filter(User.user_id == user_id).first()
        if not matched_user:
            raise APIError(status_code=404, detail="User not found.")

        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise APIError(status_code=404, detail="User profile not found.")

        decrypted_current_username = DecryptionMiddleware.decrypt({"username": matched_user.username})["username"]

        if decrypted_current_username != username:
            all_users = db.query(User).all()
            for usr in all_users:
                decrypted_username = DecryptionMiddleware.decrypt({"username": usr.username})["username"]
                if decrypted_username == username:
                    raise APIError(status_code=400, detail="Username already taken.")
            matched_user.username = EncryptionMiddleware.encrypt({"username": username})["username"]

        if bio is not None:
            profile.bio = None if bio.strip() == "" else EncryptionMiddleware.encrypt({"bio": bio})["bio"]

        image_url = None
        if profilePic:
            try:
                BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
                TEMP_DIR = os.path.join(BASE_DIR, "backend", "public", "temp")
                os.makedirs(TEMP_DIR, exist_ok=True)
                print(f"[DEBUG] Temp directory ensured at: {TEMP_DIR}")
            except Exception as folder_err:
                raise APIError(status_code=500, detail=f"Failed to create upload folder: {str(folder_err)}")

            print("[DEBUG] Starting profile picture upload...")

            file_location = os.path.join(TEMP_DIR, profilePic.filename)
            with open(file_location, "wb") as f:
                f.write(await profilePic.read())

            if profile.img:
                delete_file(profile.img)

            secure_url, public_id = upload_file(file_location)
            profile.img = EncryptionMiddleware.encrypt({"img": secure_url})["img"]
            image_url = secure_url

            print(f"[DEBUG] Image uploaded. URL: {image_url}, public_id: {public_id}")

            os.remove(file_location)

        elif profilePic is None and profile.img:
            delete_file(DecryptionMiddleware.decrypt({"img": profile.img})["img"])
            profile.img = None

        db.commit()
        db.refresh(profile)

        response_data = {
            "username": DecryptionMiddleware.decrypt({"username": matched_user.username})["username"],
            "bio": DecryptionMiddleware.decrypt({"bio": profile.bio})["bio"] if profile.bio else "",
            "img": image_url if image_url else (
                DecryptionMiddleware.decrypt({"img": profile.img})["img"] if profile.img else None
            )
        }

        print(f"[DEBUG] Sending profile update response: {response_data}")

        return APIResponse.success(
            message="Profile updated successfully",
            data=response_data
        )

    except APIError as e:
        raise e
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def delete_user_profile(user_id: str, db: Session):
    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise APIError(status_code=404, detail="User profile not found.")

        db.delete(profile)
        db.commit()

        return APIResponse.success(message="User profile deleted successfully.")

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

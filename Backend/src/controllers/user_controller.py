from sqlalchemy.orm import Session
from models.userProfile import UserProfile
from models.user import User
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from pydantic import BaseModel
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware

class UserProfileRequest(BaseModel):
    bio: str = None
    img: str = None
    blockUser: bool = False
    blockCommunity: bool = False
    blockPost: bool = False

async def create_user_profile(user_id: str, request: UserProfileRequest, db: Session):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise APIError(status_code=404, detail="User not found.")

        existing_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if existing_profile:
            raise APIError(status_code=400, detail="User profile already exists.")
        
        encrypted_data = EncryptionMiddleware.encrypt(request.model_dump())

        new_profile = UserProfile(
            user_id=user_id,
            bio=encrypted_data.get("bio"),
            img=encrypted_data.get("img"),
            blockUser=encrypted_data.get("blockUser"),
            blockCommunity=encrypted_data.get("blockCommunity"),
            blockPost=encrypted_data.get("blockPost")
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        return APIResponse.success(data=new_profile, message="User profile created successfully.")

    except APIError as e:
        raise e
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def get_user_profile(user_id: str, db: Session):
    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise APIError(status_code=404, detail="User profile not found.")
        
        decrypted_data = DecryptionMiddleware.decrypt({
            "bio": profile.bio,
            "img": profile.img,
            "blockUser": profile.blockUser,
            "blockCommunity": profile.blockCommunity,
            "blockPost": profile.blockPost
        })

        profile.bio = decrypted_data.get("bio")
        profile.img = decrypted_data.get("img")
        profile.blockUser = decrypted_data.get("blockUser")
        profile.blockCommunity = decrypted_data.get("blockCommunity")
        profile.blockPost = decrypted_data.get("blockPost")

        return APIResponse.success(data=profile, message="User profile retrieved successfully.")

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def update_user_profile(user_id: str, request: UserProfileRequest, db: Session):
    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise APIError(status_code=404, detail="User profile not found.")

        request_data = request.model_dump(exclude_unset=True)
        encrypted_data = EncryptionMiddleware.encrypt(request_data)

        for key, value in encrypted_data.items():
            setattr(profile, key, value)

        db.commit()
        db.refresh(profile)

        return APIResponse.success(data=profile, message="User profile updated successfully.")

    except APIError as e:
        raise e
    except Exception as e:
        db.rollback()
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
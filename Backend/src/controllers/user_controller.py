from sqlalchemy.orm import Session
from models.userProfile import UserProfile
from models.user import User
from models.follow import Follow  
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from pydantic import BaseModel

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

        new_profile = UserProfile(
            user_id=user_id,
            bio=request.bio,
            img=request.img,
            blockUser=request.blockUser,
            blockCommunity=request.blockCommunity,
            blockPost=request.blockPost
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        return APIResponse.success(data=new_profile, message="User profile created successfully.")

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def get_user_profile(user_id: str, db: Session):
    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise APIError(status_code=404, detail="User profile not found.")

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

        profile.bio = request.bio or profile.bio
        profile.img = request.img or profile.img
        profile.blockUser = request.blockUser
        profile.blockCommunity = request.blockCommunity
        profile.blockPost = request.blockPost

        db.commit()
        db.refresh(profile)

        return APIResponse.success(data=profile, message="User profile updated successfully.")

    except APIError as e:
        raise e
    except Exception as e:
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

async def follow_user(user_id: str, follow_id: str, db: Session):
    try:
        if user_id == follow_id:
            raise APIError(status_code=400, detail="You cannot follow yourself.")

        user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        follow_profile = db.query(UserProfile).filter(UserProfile.user_id == follow_id).first()

        if not user_profile or not follow_profile:
            raise APIError(status_code=404, detail="User not found.")

        existing_follow = db.query(Follow).filter(Follow.follower_id == user_id, Follow.followed_id == follow_id).first()
        if existing_follow:
            raise APIError(status_code=400, detail="You are already following this user.")

        new_follow = Follow(follower_id=user_id, followed_id=follow_id)
        db.add(new_follow)

        user_profile.following += 1 
        follow_profile.followers += 1  

        db.commit()
        return APIResponse.success(message=f"User {user_id} is now following {follow_id}")

    except APIError as e:
        raise e
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def unfollow_user(user_id: str, follow_id: str, db: Session):
    try:
        follow_entry = db.query(Follow).filter(Follow.follower_id == user_id, Follow.followed_id == follow_id).first()

        if not follow_entry:
            raise APIError(status_code=400, detail="You are not following this user.")

        db.delete(follow_entry)

        user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        follow_profile = db.query(UserProfile).filter(UserProfile.user_id == follow_id).first()

        if user_profile and user_profile.following > 0:
            user_profile.following -= 1  
        if follow_profile and follow_profile.followers > 0:
            follow_profile.followers -= 1 

        db.commit()
        return APIResponse.success(message=f"User {user_id} unfollowed {follow_id}")

    except APIError as e:
        raise e
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

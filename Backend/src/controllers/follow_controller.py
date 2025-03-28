from sqlalchemy.orm import Session
from models.userProfile import UserProfile
from models.follow import Follower
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse

async def follow_user(user_id: str, follow_id: str, db: Session):
    try:
        if user_id == follow_id:
            raise APIError(status_code=400, detail="You cannot follow yourself.")

        user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        follow_profile = db.query(UserProfile).filter(UserProfile.user_id == follow_id).first()

        if not user_profile or not follow_profile:
            raise APIError(status_code=404, detail="User not found.")

        existing_follow = db.query(Follower).filter(
            Follower.follower_id == user_id, 
            Follower.followed_id == follow_id
        ).first()
        if existing_follow:
            raise APIError(status_code=400, detail="You are already following this user.")

        new_follow = Follower(follower_id=user_id, followed_id=follow_id)
        db.add(new_follow)

        user_profile.following = user_profile.following + 1 if user_profile.following else 1
        follow_profile.followers = follow_profile.followers + 1 if follow_profile.followers else 1

        db.commit()
        db.refresh(new_follow)

        return APIResponse.success(message=f"User {user_id} is now following {follow_id}")

    except APIError as e:
        raise e
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def unfollow_user(user_id: str, follow_id: str, db: Session):
    try:
        follow_entry = db.query(Follower).filter(
            Follower.follower_id == user_id, 
            Follower.followed_id == follow_id
        ).first()

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
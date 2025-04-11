from sqlalchemy.orm import Session
from models.userProfile import UserProfile
from models.follow import Follower
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware

async def follow_user(user_id: str, follow_id: str, db: Session):
    try:
        if str(user_id) == str(follow_id):
            raise APIError(status_code=400, detail="You cannot follow yourself.")

        user_profile = db.query(UserProfile).filter(UserProfile.user_id == str(user_id)).first()
        follow_profile = db.query(UserProfile).filter(UserProfile.user_id == str(follow_id)).first()

        if not user_profile or not follow_profile:
            raise APIError(status_code=404, detail="User not found.")

        existing_follow = db.query(Follower).filter(
            Follower.follower_id == str(user_id),
            Follower.user_id == str(follow_id)
        ).first()
        if existing_follow:
            raise APIError(status_code=400, detail="You are already following this user.")

        new_follow = Follower(follower_id=str(user_id), user_id=str(follow_id))
        db.add(new_follow)

        decrypted_user_data = DecryptionMiddleware.decrypt({
            "following": user_profile.following
        })

        decrypted_follow_data = DecryptionMiddleware.decrypt({
            "followers": follow_profile.followers
        })

        updated_following = int(decrypted_user_data["following"] or 0) + 1
        updated_followers = int(decrypted_follow_data["followers"] or 0) + 1

        encrypted_user_data = EncryptionMiddleware.encrypt({
            "following": updated_following
        })

        encrypted_follow_data = EncryptionMiddleware.encrypt({
            "followers": updated_followers
        })

        user_profile.following = encrypted_user_data["following"]
        follow_profile.followers = encrypted_follow_data["followers"]

        db.commit()
        db.refresh(new_follow)

        return APIResponse.success(message="User {} is now following {}".format(str(user_id), str(follow_id)))

    except APIError as e:
        raise e
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail="Internal Server Error: {}".format(str(e)))


async def unfollow_user(user_id: str, follow_id: str, db: Session):
    try:
        follow_entry = db.query(Follower).filter(
            Follower.follower_id == str(user_id),
            Follower.user_id == str(follow_id)
        ).first()

        if not follow_entry:
            raise APIError(status_code=400, detail="You are not following this user.")

        db.delete(follow_entry)

        user_profile = db.query(UserProfile).filter(UserProfile.user_id == str(user_id)).first()
        follow_profile = db.query(UserProfile).filter(UserProfile.user_id == str(follow_id)).first()

        decrypted_user_data = DecryptionMiddleware.decrypt({
            "following": user_profile.following
        })

        decrypted_follow_data = DecryptionMiddleware.decrypt({
            "followers": follow_profile.followers
        })

        updated_following = max(int(decrypted_user_data["following"] or 0) - 1, 0)
        updated_followers = max(int(decrypted_follow_data["followers"] or 0) - 1, 0)

        encrypted_user_data = EncryptionMiddleware.encrypt({
            "following": updated_following
        })

        encrypted_follow_data = EncryptionMiddleware.encrypt({
            "followers": updated_followers
        })

        user_profile.following = encrypted_user_data["following"]
        follow_profile.followers = encrypted_follow_data["followers"]

        db.commit()
        return APIResponse.success(message="User {} unfollowed {}".format(str(user_id), str(follow_id)))

    except APIError as e:
        raise e
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail="Internal Server Error: {}".format(str(e)))

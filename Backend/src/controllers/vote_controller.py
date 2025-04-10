from sqlalchemy.orm import Session
from models.post import Post
from models.user import User
from models.userProfile import UserProfile
from models.vote import Vote
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware

async def add_vote_controller(post_id: str, user_id: str, vote_type: str, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise APIError(status_code=404, detail="User not found.")

        existing_vote = db.query(Vote).filter_by(post_id=post_id, user_id=user_id).first()

        post_votes = DecryptionMiddleware.decrypt({
            "upvotes": post.upvotes,
            "downvotes": post.downvotes
        })
        upvotes = int(post_votes.get("upvotes", "0"))
        downvotes = int(post_votes.get("downvotes", "0"))

        if existing_vote:
            old_vote_type = DecryptionMiddleware.decrypt({"vote_type": existing_vote.vote_type}).get("vote_type")

            if old_vote_type == vote_type:
                db.delete(existing_vote)
                if vote_type == "upvote":
                    upvotes -= 1
                    await _update_user_profile_votes(db, user_id, "total_upvotes", -1)
                else:
                    downvotes -= 1
                    await _update_user_profile_votes(db, user_id, "total_downvotes", -1)
                message = f"{vote_type.capitalize()} removed."
            else:
                encrypted_vote_type = EncryptionMiddleware.encrypt({"vote_type": vote_type}).get("vote_type")
                existing_vote.vote_type = encrypted_vote_type
                if old_vote_type == "upvote":
                    upvotes -= 1
                    await _update_user_profile_votes(db, user_id, "total_upvotes", -1)
                    downvotes += 1
                    await _update_user_profile_votes(db, user_id, "total_downvotes", 1)
                else:
                    downvotes -= 1
                    await _update_user_profile_votes(db, user_id, "total_downvotes", -1)
                    upvotes += 1
                    await _update_user_profile_votes(db, user_id, "total_upvotes", 1)
                message = f"Vote updated from {old_vote_type.capitalize()} to {vote_type.capitalize()}."
        else:
            encrypted_vote_type = EncryptionMiddleware.encrypt({"vote_type": vote_type}).get("vote_type")
            new_vote = Vote(post_id=post_id, user_id=user_id, vote_type=encrypted_vote_type)
            db.add(new_vote)
            if vote_type == "upvote":
                upvotes += 1
                await _update_user_profile_votes(db, user_id, "total_upvotes", 1)
            else:
                downvotes += 1
                await _update_user_profile_votes(db, user_id, "total_downvotes", 1)
            message = f"{vote_type.capitalize()} added."

        post.upvotes = EncryptionMiddleware.encrypt({"upvotes": str(upvotes)}).get("upvotes")
        post.downvotes = EncryptionMiddleware.encrypt({"downvotes": str(downvotes)}).get("downvotes")

        db.commit()
        return APIResponse.success(message=message)
    except APIError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def get_vote_controller(post_id: str, user_id: str, db: Session):
    try:
        vote = db.query(Vote).filter_by(post_id=post_id, user_id=user_id).first()
        post = db.query(Post).filter_by(post_id=post_id).first()

        if not post:
            raise APIError(status_code=404, detail="Post not found")

        vote_type = None
        if vote:
            vote_type = DecryptionMiddleware.decrypt({"vote_type": vote.vote_type}).get("vote_type")
        
        decrypted_upvotes = DecryptionMiddleware.decrypt({"upvotes": post.upvotes}).get("upvotes")
        decrypted_downvotes = DecryptionMiddleware.decrypt({"downvotes": post.downvotes}).get("downvotes")

        return APIResponse.success(data={
            "vote_type": vote_type,
            "upvotes": decrypted_upvotes,
            "downvotes": decrypted_downvotes
        })
        
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def _update_user_profile_votes(db: Session, user_id: str, vote_column: str, increment: int):
    try:
        user_profile = db.query(UserProfile).filter_by(user_id=user_id).first()
        if user_profile:
            decrypted_votes = DecryptionMiddleware.decrypt({vote_column: getattr(user_profile, vote_column) or EncryptionMiddleware.encrypt({"temp": "0"})["temp"]})
            current_votes = int(decrypted_votes.get(vote_column, "0"))
            new_votes = current_votes + increment
            encrypted_new_votes = EncryptionMiddleware.encrypt({vote_column: str(new_votes)}).get(vote_column)
            setattr(user_profile, vote_column, encrypted_new_votes)
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error during user profile update: {str(e)}")
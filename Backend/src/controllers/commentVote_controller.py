from sqlalchemy.orm import Session
from models.comment import Comment
from models.commentVote import CommentVote
from models.user import User
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware

async def add_vote_controller(comment_id: str, user_id: str, vote_type: str, db: Session):
    try:
        comment = db.query(Comment).filter_by(comment_id=comment_id).first()
        if not comment:
            raise APIError(status_code=404, detail="Comment not found.")

        user = db.query(User).filter_by(user_id=user_id).first()
        if not user:
            raise APIError(status_code=404, detail="User not found.")

        existing_vote = db.query(CommentVote).filter_by(comment_id=comment_id, user_id=user_id).first()

        decrypted_votes = DecryptionMiddleware.decrypt({
            "upvotes": comment.upvotes,
            "downvotes": comment.downvotes
        })
        upvotes = int(decrypted_votes.get("upvotes", "0"))
        downvotes = int(decrypted_votes.get("downvotes", "0"))

        if existing_vote:
            old_vote_type = DecryptionMiddleware.decrypt({"vote_type": existing_vote.vote_type}).get("vote_type")

            if old_vote_type == vote_type:
                db.delete(existing_vote)
                if vote_type == "upvote":
                    upvotes -= 1
                else:
                    downvotes -= 1
                message = f"{vote_type.capitalize()} removed."
            else:
                encrypted_vote_type = EncryptionMiddleware.encrypt({"vote_type": vote_type}).get("vote_type")
                existing_vote.vote_type = encrypted_vote_type
                if old_vote_type == "upvote":
                    upvotes -= 1
                    downvotes += 1
                else:
                    downvotes -= 1
                    upvotes += 1
                message = f"Vote updated from {old_vote_type} to {vote_type}."
        else:
            encrypted_vote_type = EncryptionMiddleware.encrypt({"vote_type": vote_type}).get("vote_type")
            new_vote = CommentVote(comment_id=comment_id, user_id=user_id, vote_type=encrypted_vote_type)
            db.add(new_vote)
            if vote_type == "upvote":
                upvotes += 1
            else:
                downvotes += 1
            message = f"{vote_type.capitalize()} added."

        comment.upvotes = EncryptionMiddleware.encrypt({"upvotes": str(upvotes)}).get("upvotes")
        comment.downvotes = EncryptionMiddleware.encrypt({"downvotes": str(downvotes)}).get("downvotes")

        db.commit()
        return APIResponse.success(message=message)

    except APIError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")


async def get_vote_controller(comment_id: str, user_id: str, db: Session):
    try:
        vote = db.query(CommentVote).filter_by(comment_id=comment_id, user_id=user_id).first()
        comment = db.query(Comment).filter_by(comment_id=comment_id).first()

        if not comment:
            raise APIError(status_code=404, detail="Comment not found")

        vote_type = None
        if vote:
            vote_type = DecryptionMiddleware.decrypt({"vote_type": vote.vote_type}).get("vote_type")

        decrypted_upvotes = DecryptionMiddleware.decrypt({"upvotes": comment.upvotes}).get("upvotes")
        decrypted_downvotes = DecryptionMiddleware.decrypt({"downvotes": comment.downvotes}).get("downvotes")

        return APIResponse.success(data={
            "vote_type": vote_type,
            "upvotes": decrypted_upvotes,
            "downvotes": decrypted_downvotes
        })

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
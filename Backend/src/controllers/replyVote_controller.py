from sqlalchemy.orm import Session
from models.reply import Reply
from models.voteReply import ReplyVote
from models.user import User
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware

async def add_vote_controller(reply_id: str, user_id: str, vote_type: str, db: Session):
    try:
        reply = db.query(Reply).filter_by(reply_id=reply_id).first()
        if not reply:
            raise APIError(status_code=404, detail="Reply not found.")

        user = db.query(User).filter_by(user_id=user_id).first()
        if not user:
            raise APIError(status_code=404, detail="User not found.")

        existing_vote = db.query(ReplyVote).filter_by(reply_id=reply_id, user_id=user_id).first()

        decrypted = DecryptionMiddleware.decrypt({
            "upvotes": reply.upvotes,
            "downvotes": reply.downvotes
        })
        upvotes = int(decrypted.get("upvotes") or "0")
        downvotes = int(decrypted.get("downvotes") or "0")

        if not existing_vote:
            encrypted_vote = EncryptionMiddleware.encrypt({"vote_type": vote_type}).get("vote_type")
            db.add(ReplyVote(reply_id=reply_id, user_id=user_id, vote_type=encrypted_vote))

            if vote_type == "upvote":
                upvotes += 1
            else:
                downvotes += 1

            message = f"{vote_type.capitalize()} added."

        else:
            existing_type = DecryptionMiddleware.decrypt({"vote_type": existing_vote.vote_type}).get("vote_type")

            if existing_type == vote_type:
                db.delete(existing_vote)

                if vote_type == "upvote":
                    upvotes -= 1
                else:
                    downvotes -= 1

                message = f"{vote_type.capitalize()} removed."

            else:
                encrypted_vote = EncryptionMiddleware.encrypt({"vote_type": vote_type}).get("vote_type")
                existing_vote.vote_type = encrypted_vote

                if vote_type == "upvote":
                    upvotes += 1
                    downvotes -= 1
                else:
                    downvotes += 1
                    upvotes -= 1

                message = f"Vote updated from {existing_type} to {vote_type}."

        reply.upvotes = EncryptionMiddleware.encrypt({"upvotes": str(upvotes)}).get("upvotes")
        reply.downvotes = EncryptionMiddleware.encrypt({"downvotes": str(downvotes)}).get("downvotes")

        db.commit()

        return APIResponse.success(data={
            "message": message,
            "upvotes": str(upvotes),
            "downvotes": str(downvotes)
        })

    except APIError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")


async def get_vote_controller(reply_id: str, user_id: str, db: Session):
    try:
        reply = db.query(Reply).filter_by(reply_id=reply_id).first()
        if not reply:
            raise APIError(status_code=404, detail="Reply not found.")

        vote = db.query(ReplyVote).filter_by(reply_id=reply_id, user_id=user_id).first()
        vote_type = None
        if vote:
            vote_type = DecryptionMiddleware.decrypt({"vote_type": vote.vote_type}).get("vote_type")

        decrypted = DecryptionMiddleware.decrypt({
            "upvotes": reply.upvotes,
            "downvotes": reply.downvotes
        })

        return APIResponse.success(data={
            "vote_type": vote_type,
            "upvotes": decrypted.get("upvotes") or "0",
            "downvotes": decrypted.get("downvotes") or "0"
        })

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

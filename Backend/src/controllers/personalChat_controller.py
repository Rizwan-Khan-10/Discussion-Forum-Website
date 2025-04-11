import json
from sqlalchemy.orm import Session
from models.personalChat import PersonalChat
from models.user import User
from models.userProfile import UserProfile
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.decryption import DecryptionMiddleware

async def get_personal_chats(current_user_id: str, db: Session):
    try:
        chats = db.query(PersonalChat).filter(
            (PersonalChat.user_id == current_user_id) |
            (PersonalChat.user_list.contains([current_user_id]))
        ).all()

        if not chats:
            raise APIError(status_code=404, detail="No personal chats found.")

        result = []

        for chat in chats:
            if chat.user_id == current_user_id:
                for other_id in chat.user_list:
                    if other_id == current_user_id:
                        continue  # 👈 Skip current user itself

                    user = db.query(User).filter(User.user_id == other_id).first()
                    profile = db.query(UserProfile).filter(UserProfile.user_id == other_id).first()
                    if not user or not profile:
                        continue

                    last_msg = None
                    if chat.last_message:
                        try:
                            encrypted_dict = json.loads(chat.last_message)
                            decrypted = DecryptionMiddleware.decrypt(encrypted_dict)
                            last_msg = decrypted.get("message")
                        except Exception:
                            last_msg = None

                    result.append({
                        "user_id": other_id,
                        "username": DecryptionMiddleware.decrypt({"username": user.username}).get("username"),
                        "img": DecryptionMiddleware.decrypt({"img": profile.img}).get("img"),
                        "last_message": last_msg
                    })
            else:
                if chat.user_id == current_user_id:
                    continue 

                owner = db.query(User).filter(User.user_id == chat.user_id).first()
                profile = db.query(UserProfile).filter(UserProfile.user_id == chat.user_id).first()
                if not owner or not profile:
                    continue

                last_msg = None
                if chat.last_message:
                    try:
                        encrypted_dict = json.loads(chat.last_message)
                        decrypted = DecryptionMiddleware.decrypt(encrypted_dict)
                        last_msg = decrypted.get("message")
                    except Exception:
                        last_msg = None

                result.append({
                    "user_id": chat.user_id,
                    "username": DecryptionMiddleware.decrypt({"username": owner.username}).get("username"),
                    "img": DecryptionMiddleware.decrypt({"img": profile.img}).get("img"),
                    "last_message": last_msg
                })

        return APIResponse.success(data=result, message="Personal chats retrieved successfully.")

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

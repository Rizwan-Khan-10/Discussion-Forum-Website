import os
import uuid
import datetime
from sqlalchemy.orm import Session
from models.user import User
from middlewares.encryption import EncryptionMiddleware  
from middlewares.decryption import DecryptionMiddleware  
from middlewares.hassing import hash_password, verify_password  
from utils.ApiError import APIError  
from utils.ApiResponse import APIResponse  
from models.userProfile import UserProfile

async def register_user(request, db: Session):
    try:
        existing_user = db.query(User).filter(
            (User.email == request.email) | (User.username == request.username)
        ).first()

        if existing_user:
            if existing_user.email == request.email:
                raise APIError(status_code=400, detail="Email already registered.")
            if existing_user.username == request.username:
                raise APIError(status_code=400, detail="Username already taken.")

        encrypted_data = EncryptionMiddleware.encrypt({
            "username": request.username,
            "email": request.email
        })

        raw_user_id = str(uuid.uuid4())
        encrypted_user_id = EncryptionMiddleware.encrypt({"user_id": raw_user_id})["user_id"]

        new_user = User(
            user_id=encrypted_user_id,
            username=encrypted_data["username"],
            email=encrypted_data["email"],
            password=hash_password(request.password),
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )

        db.add(new_user)
        db.commit()

        encrypted_profile_data = EncryptionMiddleware.encrypt({
            "bio": "",
            "img": "",
            "followers": "0",
            "following": "0",
            "total_posts": "0",
            "total_upvotes": "0",
            "total_downvotes": "0",
            "reputation": "10",
            "total_bookmarks": "0",
            "total_shares": "0",
            "total_views": "0",
            "blockUser": "",
            "blockCommunity": "",
            "blockPost": ""
        })

        user_profile = UserProfile(
            user_id=encrypted_user_id,
            bio=encrypted_profile_data["bio"],
            img=encrypted_profile_data["img"],
            followers=encrypted_profile_data["followers"],
            following=encrypted_profile_data["following"],
            total_posts=encrypted_profile_data["total_posts"],
            total_upvotes=encrypted_profile_data["total_upvotes"],
            total_downvotes=encrypted_profile_data["total_downvotes"],
            reputation=encrypted_profile_data["reputation"],
            total_bookmarks=encrypted_profile_data["total_bookmarks"],
            total_shares=encrypted_profile_data["total_shares"],
            total_views=encrypted_profile_data["total_views"],
            blockUser=encrypted_profile_data["blockUser"],
            blockCommunity=encrypted_profile_data["blockCommunity"],
            blockPost=encrypted_profile_data["blockPost"]
        )

        db.add(user_profile)
        db.commit()

        return APIResponse.success(message="User registered successfully")

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def authenticate_user(request, db: Session):
    try:
        users = db.query(User).all()
        matched_user = None

        for user in users:
            try:
                decrypted_email = DecryptionMiddleware.decrypt({"email": user.email})["email"]
                if decrypted_email == request.email:
                    matched_user = user
                    break
            except Exception:
                continue  

        if not matched_user or not verify_password(request.password, matched_user.password):
            raise APIError(status_code=401, detail="Invalid email or password.")

        decrypt_data = DecryptionMiddleware.decrypt({
            "username": matched_user.username,
            "user_id": matched_user.user_id
        })

        return APIResponse.success(
            data={
                "user_id": decrypt_data["user_id"],
                "username": decrypt_data["username"]
            }, 
            message="Login successful"
        )

    except APIError as e:
        raise e  
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

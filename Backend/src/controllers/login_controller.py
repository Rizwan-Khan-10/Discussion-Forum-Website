import os
import datetime
import jwt
from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from models.user import User
from middlewares.encryption import EncryptionMiddleware  
from middlewares.hassing import hash_password, verify_password  
from utils.ApiError import APIError  
from utils.ApiResponse import APIResponse  

SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

async def register_user(request, db: Session):
    try:
        existing_user = db.query(User).filter((User.email == request.email) | (User.name == request.username)).first()
        if existing_user:
            if existing_user.email == request.email:
                raise APIError(status_code=400, detail="Email already registered.")
            if existing_user.name == request.username:
                raise APIError(status_code=400, detail="Username already taken.")

        new_user = User(
            name=request.username,
            email=request.email,
            password=hash_password(request.password),
            created_at=datetime.datetime.now(datetime.timezone.utc)  
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        encrypted_user_id = EncryptionMiddleware.encrypt({"user_id": new_user.user_id})
        new_user.user_id = encrypted_user_id["user_id"]
        db.commit()

        return APIResponse.success(data={"user_id": encrypted_user_id["user_id"]}, message="User registered successfully")

    except APIError as e:
        raise e  
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def generate_tokens(user_id):
    refresh_token_payload = {
        "sub": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)  # ✅ Proper UTC time
    }
    refresh_token = jwt.encode(refresh_token_payload, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    access_token_payload = {
        "sub": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)  # ✅ Proper UTC time
    }
    access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": access_token, "refresh_token": refresh_token}

async def authenticate_user(request, db: Session):
    try:
        user = db.query(User).filter(User.email == request.email).first()
        if not user or not verify_password(request.password, user.password):
            raise APIError(status_code=401, detail="Invalid email or password.")

        tokens = await generate_tokens(user.user_id)

        encrypted_access_token = EncryptionMiddleware.encrypt({"access_token": tokens["access_token"]})
        encrypted_refresh_token = EncryptionMiddleware.encrypt({"refresh_token": tokens["refresh_token"]})

        user.access_token = encrypted_access_token["access_token"]  
        user.refresh_token = encrypted_refresh_token["refresh_token"]  
        db.commit()

        return APIResponse.success(
            data={"access_token": tokens["access_token"]}, 
            message="Login successful"
        )
    
    except APIError as e:
        raise e  
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

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
ALGORITHM = os.getenv("ALGORITHM")

async def register_user(request, db: Session):
    try:
        existing_user = db.query(User).filter((User.email == request.email) | (User.name == request.username)).first()
        if existing_user:
            if existing_user.email == request.email:
                raise APIError(status_code=400, detail="Email already registered.")
            if existing_user.name == request.username:
                raise APIError(status_code=400, detail="Username already taken.")

        encrypted_password = EncryptionMiddleware.encrypt({
            "password": hash_password(request.password)
        })["password"]

        new_user = User(
            name=request.username,
            email=request.email,
            password=encrypted_password,
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return APIResponse.success(data={"user_id": new_user.user_id}, message="User registered successfully")

    except APIError as e:
        raise e  
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def authenticate_user(request, db: Session):
    try:
        user = db.query(User).filter(User.email == request.email).first()
        if not user or not verify_password(request.password, user.password):
            raise APIError(status_code=401, detail="Invalid email or password.")

        token_payload = {
            "sub": user.user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

        user.access_token = token  
        db.commit()

        return APIResponse.success(data={"access_token": token}, message="Login successful")

    except APIError as e:
        raise e  
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

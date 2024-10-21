from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status

from app.db.models.users import Users
from app.core import config


settings = config.Settings()

bcryt_content = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def hash_password(plain_password: str):
    return bcryt_content.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str):
    return bcryt_content.verify(plain_password, hashed_password)


def autenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(
                detail="could not validate user",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return {"username": username, "id": user_id, "role": user_role}

    except JWTError:
        raise HTTPException(
            detail="could not validate user",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

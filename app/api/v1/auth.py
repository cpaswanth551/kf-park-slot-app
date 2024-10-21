from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (
    autenticate_user,
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.db.base import get_db
from app.db.crud import users
from app.db.models.users import Users
from app.schemas.users import CreateUserRequest, UserVerification


router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

otp_storage = {}


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = autenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            detail="could not validate user", status_code=status.HTTP_401_UNAUTHORIZED
        )

    token = create_access_token(
        user.username, user.id, role=user.role, expires_delta=timedelta(minutes=29)
    )

    return {"access_token": token, "token_type": "bearer"}


@router.post("/")
async def create_user(user: CreateUserRequest, db: db_dependency):
    return users.create_user(db, user)


@router.get("/me")
async def read_user(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Autentication Failed"
        )

    user_id = int(user.get("id"))

    return users.get_user(db, user_id)


@router.post("/password/", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(
    db: db_dependency, user: user_dependency, user_verification: UserVerification
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Autentication Failed"
        )

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not verify_password(user_verification.password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Error on password"
        )

    user_model.hashed_password = hash_password(user_verification.new_password)
    db.add(user_model)
    db.commit()

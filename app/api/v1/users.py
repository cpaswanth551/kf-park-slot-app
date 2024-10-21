from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.base import get_db
from app.schemas.users import UserDisplay
from app.db.crud import users


router = APIRouter(prefix="/api/v1/users", tags=["Users"])


db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", response_model=List[UserDisplay])
async def get_all_users(db: db_dependency, user: user_dependency):
    return users.read_users(db)


@router.get("/{user_id}", response_model=UserDisplay)
async def get_user(db: db_dependency, user_id: int, user: user_dependency):
    return users.get_user(db, user_id)

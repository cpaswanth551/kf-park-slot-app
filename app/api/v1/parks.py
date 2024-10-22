from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.authorizations import authorize
from app.core.security import get_current_user
from app.db.base import get_db
from app.db.models.parks import *
from app.schemas.parks import CreatePlaceRequest, PlaceDisplay, SlotDisplay
from app.db.crud import parks

router = APIRouter(prefix="/api/v1/park", tags=["Park"])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/places")
@authorize(role=["admin", "superadmin"])
async def create_place(
    place: CreatePlaceRequest, db: db_dependency, current_user: user_dependency
):
    return parks.create_places(db, place)


@router.get("/places")
async def read_places(db: db_dependency):
    return parks.get_all_places(db)


@router.get("/places/{place_id}", response_model=PlaceDisplay)
async def read_place(db: db_dependency, place_id: int):
    return parks.get_place(db, place_id)


@router.get("/slot/{slot_number}", response_model=SlotDisplay)
async def read_place(db: db_dependency, slot_number: str):
    return parks.get_slot(db, slot_number)

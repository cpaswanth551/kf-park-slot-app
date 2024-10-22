from sqlalchemy.orm import Session

from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends

from app.core.security import get_current_user
from app.db.base import get_db
from app.db.crud import reservations
from app.schemas.parks import CreateReservationRequest


router = APIRouter(prefix="/api/v1/reservations", tags=["Reservations"])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/")
async def create_reservations(reservation: CreateReservationRequest, db: db_dependency):
    return reservations.create_reservations(db, reservation)


@router.get("/")
async def read_reservations(db: db_dependency, current_user: user_dependency):
    return reservations.get_reservation(db, current_user.id)

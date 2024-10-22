from sqlalchemy.orm import Session

from typing import Annotated, List
from fastapi import APIRouter
from fastapi.params import Depends

from app.core.security import get_current_user
from app.db.base import get_db
from app.db.crud import reservations
from app.schemas.parks import CreateReservationRequest, ReservationDisplay


router = APIRouter(prefix="/api/v1/reservations", tags=["Reservations"])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/")
async def create_reservations(reservation: CreateReservationRequest, db: db_dependency):
    return reservations.create_reservations(db, reservation)


@router.get("/", response_model=List[ReservationDisplay])
async def read_reservations(db: db_dependency, current_user: user_dependency):
    reservations_list = reservations.get_reservation(db, current_user.get("id"))
    response = []
    for reservation in reservations_list:
        response.append(
            {
                "time_reserved": reservation.time_reserved,
                "phone_number": reservation.phone_number,
                "slot": {
                    "id": reservation.slot.id,
                    "slot_number": reservation.slot.slot_number,
                    "price": str(reservation.slot.price),
                    "place": {
                        "name": reservation.slot.place.name,
                        "address": reservation.slot.place.address,
                        "total_slots": reservation.slot.place.total_slots,
                    },
                },
            }
        )

    return response

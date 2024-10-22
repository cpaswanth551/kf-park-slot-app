from sqlalchemy.orm import Session
import datetime
from app.db.models.parks import Places, Reservations, Slots
from app.schemas.parks import CreateReservationRequest


def create_reservations(
    db: Session, create_reservation_model: CreateReservationRequest
):
    create_reserveration_model = Reservations(
        reservation_time=datetime.datetime.now(),
        time_reserved=create_reservation_model.time_reserved,
        phone_number=create_reservation_model.phone_number,
        status="pending",
        slot_id=create_reservation_model.slot_id,
        user_id=create_reservation_model.user_id,
    )

    db.add(create_reserveration_model)
    slot = db.query(Slots).filter(Slots.id == create_reservation_model.slot_id).first()
    if slot:
        slot.is_booked = True
    db.commit()

    db.refresh(create_reserveration_model)
    return create_reserveration_model


def get_reservation(db: Session, user_id: int):
    return (
        db.query(Reservations)
        .join(Slots)
        .join(Places)
        .filter(Reservations.user_id == user_id)
        .all()
    )

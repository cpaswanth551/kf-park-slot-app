from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.parks import Places, Slots
from app.schemas.parks import (
    CreatePlaceRequest,
    CreateSlotsRequest,
    SlotDisplay,
    SlotPlace,
)


def create_places(db: Session, create_place_request: CreatePlaceRequest):
    create_place_model = Places(
        name=create_place_request.name,
        address=create_place_request.address,
        total_slots=create_place_request.total_slots,
    )

    db.add(create_place_model)
    db.flush()

    slots = [
        Slots(
            slot_number=f"{create_place_model.name[:3]}{create_place_model.id}0{i + 1}",
            price=10.0,
            is_booked=False,
            place_id=create_place_model.id,
        )
        for i in range(create_place_model.total_slots)
    ]
    db.add_all(slots)

    db.commit()
    db.refresh(create_place_model)
    return create_place_model


def create_slot(db: Session, create_slot_request: CreateSlotsRequest):
    create_slot_model = Slots(
        slot_number=create_slot_request.slot_number,
        price=create_slot_request.price,
        is_booked=False,
        place_id=create_slot_request.place_id,
    )

    db.add(create_slot_model)
    db.commit()
    db.refresh(create_slot_model)
    return create_slot_model


def get_all_places(db: Session):
    return db.query(Places).all()


def get_place(db: Session, id: int):
    place = db.query(Places).filter(Places.id == id).first()
    if not place:
        return HTTPException(detail="place not found", status_code=401)

    slots = [
        SlotPlace(slot_number=slot.slot_number, price=str(slot.price))
        for slot in place.slot
    ]

    return {
        "name": place.name,
        "address": place.address,
        "total_slots": len(slots),
        "slots": slots,
    }


def get_slot(db: Session, slot_number: str):
    slot = db.query(Slots).filter(Slots.slot_number == slot_number).first()
    if not slot:
        return HTTPException(detail="slot not found", status_code=401)

    return {
        "id": slot.id,
        "slot_number": slot.slot_number,
        "price": str(slot.price),
        "place": slot.place,
    }

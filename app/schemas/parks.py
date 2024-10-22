from typing import List
from pydantic import BaseModel, Field, constr


class CreatePlaceRequest(BaseModel):
    name: str = Field(min_length=4)
    address: str = Field(min_length=4)
    total_slots: int


class CreateSlotsRequest(BaseModel):
    slot_number: str
    price: str
    place_id: int


class SlotPlace(BaseModel):
    slot_number: str
    price: str


class PlaceDisplay(BaseModel):
    name: str
    address: str
    total_slots: int

    slots: List[SlotPlace]


class PlaceSlot(BaseModel):
    name: str
    address: str


class SlotDisplay(BaseModel):
    slot_number: str
    price: str

    place: PlaceSlot

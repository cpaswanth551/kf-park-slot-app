from pydantic import BaseModel, Field, constr


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

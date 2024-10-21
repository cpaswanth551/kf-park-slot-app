from app.db.models.users import Users
from app.schemas.users import CreateUserRequest
from app.core.security import hash_password
from sqlalchemy.orm import Session


def create_user(db: Session, create_user_request: CreateUserRequest):
    create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=hash_password(create_user_request.password),
        is_active=True,
        role=create_user_request.role,
        phone_number=create_user_request.phone_number,
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return create_user_model


def read_users(db: Session):
    return db.query(Users).all()


def get_user(db: Session, id: int):
    return db.query(Users).filter(Users.id == id).first()

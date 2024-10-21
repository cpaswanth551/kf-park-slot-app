from .utils import *
from app.core.security import *


def test_autenticate_user(test_user):

    db = TestingSessionLocal()

    autenticated_user = autenticate_user(
        test_user.username, test_user.hashed_password, db=db
    )

    autenticated_user = autenticate_user(test_user.username, "testpassword", db)
    assert autenticated_user is not None
    assert autenticated_user.username == test_user.username

    non_existing_user = autenticate_user("wronguser", "testpassword", db)
    assert non_existing_user is False

    wrong_password_user = autenticate_user(test_user.username, "wrongpassword", db)
    assert wrong_password_user is False


def test_create_access_token():
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decode_token = jwt.decode(
        token, SECRET_KEY, ALGORITHM, options={"verify_signature": False}
    )

    assert decode_token["sub"] == username


def test_hash_password():
    plain_password = "test123"

    hashed_password = hash_password(plain_password)

    assert verify_password(plain_password, hashed_password) == True


def test_verify_password(test_user):
    assert verify_password("testpassword", test_user.hashed_password) is True
    assert verify_password("wrong", test_user.hashed_password) is False


@pytest.mark.asyncio
async def test_get_current_user():
    encode = {"sub": "testuser", "id": 1, "role": "admin"}

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)

    assert user == {"username": "testuser", "id": 1, "role": "admin"}

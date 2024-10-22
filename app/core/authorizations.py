from functools import wraps
from fastapi import HTTPException, status


def authorize(role: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not authenticated",
                )
            user_role = kwargs.get("current_user")["role"]
            if user_role not in role:
                raise HTTPException(
                    detail="User not authorized to perform this action",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
            return await func(*args, **kwargs)

        return wrapper

    return decorator

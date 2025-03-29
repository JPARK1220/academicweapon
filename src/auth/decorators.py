from functools import wraps
from fastapi import HTTPException, status, Request

from src.auth.models import User
from .dependencies import AuthDependencies


def auth_guard(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Find the request object
        request = None
        for arg in args:
            if hasattr(arg, "headers"):
                request = arg
                break

        if not request:
            for key, value in kwargs.items():
                if hasattr(value, "headers"):
                    request = value
                    break

        if not request:
            raise ValueError("Request object not found in function arguments")

        # Extract token from headers
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header.replace("Bearer ", "")

        # Get auth service and verify token
        auth_service = AuthDependencies.get_auth_service()
        user = await auth_service.get_current_user_by_token(token)

        # Store user in request.state instead of kwargs
        request.state.user = user

        return await func(*args, **kwargs)

    return wrapper

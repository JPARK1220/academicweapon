from fastapi import Depends
from fastapi import security
from fastapi.security import HTTPAuthorizationCredentials

from .models import User
from .service import AuthService

async def get_auth_service():
    return AuthService()

async def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """
    FastAPI dependency that extracts and verifies the JWT token from the request headers.
    Can be used with FastAPI's dependency injection system.

    Usage:
        @app.get("/api/me")
        async def get_user_info(current_user: User = Depends(AuthDependencies.get_authenticated_user)):
            return current_user

    Args:
        credentials: The HTTP authorization credentials extracted by FastAPI

    Returns:
        User: The authenticated user information
    """
    token = credentials.credentials

    # Use the AuthService to get the user
    auth_service: AuthService = get_auth_service()
    return await auth_service.get_current_user_by_token(token)

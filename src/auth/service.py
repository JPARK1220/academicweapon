from fastapi import Depends, HTTPException, status, security
from fastapi.security import HTTPAuthorizationCredentials
from src.database import get_supabase
from .models import RefreshRequest, RefreshResponse, SignupResponse, User, UserSignup, LoginRequest


class AuthService:
    def __init__(self):
        pass

    async def signUp(self, user_data: UserSignup):
        try:
            supabase = get_supabase()
            response = await supabase.auth.sign_up(
                {
                    "email": user_data.email,
                    "password": user_data.password,
                    "options": {"data": {"name": user_data.name}},
                }
            )

            if response.user:
                return SignupResponse(
                    user_id=response.user.id,
                    message="User registered successfully. Check your email for confirmation.",
                    success=True,
                )
            else:
                return SignupResponse(message="Registration failed", success=False)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Registration error: {str(e)}",
            )

    async def login(self, login_data: LoginRequest):
        try:
            supabase = get_supabase()
            response = await supabase.auth.sign_in_with_password(
                {"email": login_data.email, "password": login_data.password}
            )

            if response.user:
                return {
                    "token_type": "bearer",
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                    "token_type": "bearer",
                    "user": response.user,
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Login failed: {str(e)}",
            )

    async def get_current_user(
        self, credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User:
        token = credentials.credentials

        # Get Supabase client
        supabase = get_supabase()
        if not supabase:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Supabase client not initialized",
            )

        try:
            user = await supabase.auth.get_user(token)
            return User(
                id=user.user.id,
                email=user.user.email,
                user_metadata=user.user.user_metadata,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def get_current_user_by_token(self, token: str) -> User:
        # Get Supabase client
        supabase = get_supabase()
        if not supabase:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Supabase client not initialized",
            )

        try:
            user = await supabase.auth.get_user(token)
            return User(
                id=user.user.id,
                email=user.user.email,
                user_metadata=user.user.user_metadata,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
    async def refresh_token(self, refresh_data: RefreshRequest):
        supabase = get_supabase()
        try:
            response = await supabase.auth.refresh_session(refresh_data.refresh_token)

            return RefreshResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                token_type="bearer",
                expires_in=response.session.expires_in,
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid refresh token"  # Corrected 'detail' parameter
            )

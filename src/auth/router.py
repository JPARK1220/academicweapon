from .service import AuthService
from .decorators import auth_guard
from .dependencies import get_auth_service
from .models import LoginRequest, RefreshResponse, RefreshRequest, SignupResponse, UserSignup
from fastapi import APIRouter, Depends, Request
from fastapi_utils.cbv import cbv

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=SignupResponse)
async def signUp(
    user_data: UserSignup,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.signUp(user_data)

@router.post("/login")
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.login(login_data)

@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(
    refresh_data: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.refresh_token(refresh_data)

@router.get("/me")
@auth_guard
async def get_user_profile(request: Request):
    user = request.state.user
    return {
        "message": "You are authenticated!",  # Temporary message
        "user_id": user.id,
        "email": user.email,
    }

from .service import AuthService
from .models import LoginRequest, SignupResponse, UserSignup
from fastapi import APIRouter, Depends

router = APIRouter()

def get_auth_service():
  return AuthService

@router.post("/signup", response_model=SignupResponse)
async def signUp(user_data: UserSignup, auth_service = Depends(get_auth_service)):
  return await auth_service.signUp(user_data)

@router.post("/login")
async def login(login_data: LoginRequest, auth_service = Depends(get_auth_service)):
  return await auth_service.login(login_data)
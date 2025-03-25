from .decorators import auth_guard
from .dependencies import AuthDependencies
from .models import LoginRequest, SignupResponse, User, UserSignup
from fastapi import APIRouter, Depends, Request


class AuthRouter:
  router = APIRouter()

  @router.post("/signup", response_model=SignupResponse)
  async def signUp(user_data: UserSignup, auth_service = Depends(AuthDependencies.get_auth_service)):
    return await auth_service.signUp(user_data)

  @router.post("/login")
  async def login(login_data: LoginRequest, auth_service = Depends(AuthDependencies.get_auth_service)):
    return await auth_service.login(login_data)
  
  @router.get("/me")
  @auth_guard
  async def get_user_profile(request: Request):
    user = request.state.user
    return {
        "message": "You are authenticated!", # Temporary message
        "user_id": user.id,
        "email": user.email
    }

auth_router = AuthRouter().router
from .service import AuthService
from .decorators import auth_guard
from .dependencies import AuthDependencies
from .models import LoginRequest, RefreshResponse, RefreshRequest, SignupResponse, User, UserSignup
from fastapi import APIRouter, Depends, Request
from fastapi_utils.cbv import cbv

router = APIRouter(prefix="/auth", tags=["authentication"])

@cbv(router)
class AuthRouter:
    auth_service: AuthService = Depends(AuthDependencies.get_auth_service)

    @router.post("/signup", response_model=SignupResponse)
    async def signUp(
        self,
        user_data: UserSignup,
    ):
        return await self.auth_service.signUp(user_data)

    @router.post("/login")
    async def login(
        self,
        login_data: LoginRequest,
    ):
        return await self.auth_service.login(login_data)
    
    @router.post("/refresh", response_model=RefreshResponse)
    @auth_guard
    async def refresh_token(
        self,
        refresh_data: RefreshRequest,
    ):
        return await self.auth_service.refresh_token(refresh_data)

    @router.get("/me")
    @auth_guard
    async def get_user_profile(self, request: Request):
        user = request.state.user
        return {
            "message": "You are authenticated!",  # Temporary message
            "user_id": user.id,
            "email": user.email,
        }

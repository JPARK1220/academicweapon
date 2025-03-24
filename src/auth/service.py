from fastapi import HTTPException, status
from src.database import get_supabase
from .models import SignupResponse, UserSignup, LoginRequest


class AuthService:
  def __init__(self):
    pass

  async def signUp(user_data: UserSignup):
    try:
      supabase = get_supabase()
      response = await supabase.auth.sign_up({
          "email": user_data.email,
          "password": user_data.password,
          "options": {"data": {"name": user_data.name}}
      })
  
      if response.user:
          return SignupResponse(
              user_id=response.user.id,
              message="User registered successfully. Check your email for confirmation.",
              success=True
          )
      else:
          return SignupResponse(
              message="Registration failed",
              success=False
          )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration error: {str(e)}"
        )
    
  async def login(login_data: LoginRequest):
    try:
      supabase = get_supabase()
      response = await supabase.auth.sign_in_with_password({
          "email": login_data.email,
          "password": login_data.password
      })
      
      if response.user:
          return {
              "access_token": response.session.access_token,
              "token_type": "bearer",
              "user": response.user
          }
      else:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid credentials"
          )
    except Exception as e:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail=f"Login failed: {str(e)}"
      )
       
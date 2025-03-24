
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class SignupResponse(BaseModel):
    user_id: Optional[str] = None
    message: str
    success: bool

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

from typing import Any, Dict, Optional
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

class User(BaseModel):
  id: str
  email: Optional[str] = None
  user_metadata: Optional[Dict[str, Any]] = None
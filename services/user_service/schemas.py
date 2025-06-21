from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"
    support = "support"

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    preferences: Optional[List[str]] = []
    role: UserRole = UserRole.user
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
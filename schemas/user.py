from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class Users(BaseModel):
    users: list[User]


class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[User | Users] = None

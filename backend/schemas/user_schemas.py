import os
from enum import Enum
from typing import Optional
import uuid
from pydantic.networks import EmailStr
from pydantic import BaseModel

from dotenv import load_dotenv


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv('JWT_SECRET_KEY')


class TitleEnum(str, Enum):
    mrs: str = 'Mrs'
    mr: str = 'Mr'
    ms: str = 'Ms'


class RegisterUserSchema(BaseModel):
    title: str
    username: str
    full_name: str
    phone: str
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    id: uuid.UUID
    title: TitleEnum
    username: str
    full_name: str
    phone: str
    email: EmailStr
    is_admin: bool
    is_staff: bool


class EditUserSchema(BaseModel):
    title: Optional[TitleEnum]
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    is_admin: Optional[bool]
    is_staff: Optional[bool]


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str

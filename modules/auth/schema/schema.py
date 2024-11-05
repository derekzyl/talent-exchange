from datetime import datetime
from enum import Enum, unique
from pydantic import BaseModel, EmailStr

from modules.general_crud.crud_schema import PermissionE


class User(BaseModel):
    email: EmailStr
    username: str


class UserSignupSchema(User):
    password: str
    confirm_password: str


@unique
class RoleE(str, Enum):
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"
    STAFF = "STAFF"
    MAVEN = "MAVEN"


class PresenceE(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    AWAY = "AWAY"


class TokenTypeE(str, Enum):
    EMAIL = "em"
    Password = "ps"


class UserInDbSchema(User):
    id: str
    is_email_verified: bool
    token: str
    token_expiry_time: datetime
    password: str
    presence: PresenceE
    permission: list[PermissionE]
    role: RoleE
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode: bool = True


@unique
class VisibleE(str, Enum):
    AVAILABLE = "AVAILABLE"


class ExperienceLevel(str, Enum):
    ENTRY = "ENTRY"
    INTERMEDIATE = "INTERMEDIATE"
    EXPERT = "EXPERT"


class UserProfile(BaseModel):
    visibility: str


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class ResetPassword(BaseModel):
    email: str

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import NotRequired, Optional, TypedDict

from app.core import business


@dataclass
class UserBusD:
    id: str

    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    language: str 
    remember_token: str
    deleted_at: datetime
    created_at: datetime 
    updated_at: datetime 
    is_commission_agent: bool
    commission_agent_id: str
    business_id: Optional[int]
    allow_login: bool
    user_type:str
    gender:str


class UserBusT(TypedDict, ):
    id: str

    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    language: str

    signup_type: str # Either 'email' or 'phone' GOOGLE or FACEBOOK
    remember_token: str
    deleted_at: datetime
    created_at: datetime 
    updated_at: datetime 
    is_commission_agent: bool
    commission_agent_id: str
    business_id: int
    allow_login: bool
    user_type:str
    gender:str
class CreateBusUserT(TypedDict ):


    first_name: str
    last_name: str
    username: NotRequired[str]
    email: str
    password: str
    language: NotRequired[str]

    signup_type: str # Either 'email' or 'phone' GOOGLE or FACEBOOK

    is_commission_agent: bool
    commission_agent_id: NotRequired[str]
    business_id: NotRequired[int]
    allow_login: NotRequired[bool]
    user_type:NotRequired[str]
    gender:NotRequired[str]


class UpdateUserT(TypedDict ):
    first_name: str
    last_name: str
    username: NotRequired[str]

    language: NotRequired[str]
    remember_token: NotRequired[str]

    gender:NotRequired[str]


class GenderE(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class UserTypeE(Enum):
    CUSTOMER = "customer"
    BUSINESS = "business"
    AGENT = "agent"
    STAFF='STAFF'
    API_USER='API_USER'
    SUPER_ADMIN = "super_admin"
    COMMISSION_AGENT= "commission_agent"


@dataclass    
class CreateUserD:

    first_name: str
    last_name: str
    email: str
    password: str



class RegisterBusUserT(TypedDict ):

    first_name: str
    last_name: str
    email: str
    password: str
    business_id: int



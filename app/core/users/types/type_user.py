
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from typing import NotRequired, Optional, TypedDict


@dataclass
class UserD:
    id: str

    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    language: str 
    deleted_at: datetime
    created_at: datetime 
    updated_at: datetime 

    allow_login: bool
  
    gender:str


class UserT(TypedDict, ):
    id: str

    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    language: str 
    deleted_at: datetime
    created_at: datetime 
    updated_at: datetime 
    country:str
    region:str

    allow_login: bool
  
    gender:str
class CreateUserT(TypedDict ):


    first_name: str
    last_name: str
    
    country:str
    region:str
    email: str
    password: str
class LoginUserT(TypedDict ):
    email: str
    password: str


class ForgotPasswordT(TypedDict ):
    email: str    




    
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



@dataclass    
class CreateUserD:


    first_name: str
    last_name: str
    email: str
    password: str


    
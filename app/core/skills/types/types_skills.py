from typing import TypedDict
from enum import Enum


class enum_skill_level(Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"


class enum_available_day(Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"
class SkillT(TypedDict):
    id:str
    skill_category: str
    skill_name: str
    skill_description: str
    skill_level: enum_skill_level

    
    user_id:str
    created_at:str
    updated_at:str
    deleted_at:str
class CreateTimeT(TypedDict):
    available_day:str
    start_time:str
    end_time:str


    
class CreateSkillT(TypedDict, ):
    skill_category: str
    skill_name: str
    skill_description: str
    skill_level: enum_skill_level
    available_times: list[CreateTimeT] | None

    user_id:str

    
    
class CreateNewSkillT(TypedDict, ):
    skill_category: str
    skill_name: str
    skill_description: str
    skill_level: enum_skill_level
    available_times: list[CreateTimeT] | None


    

    


class UpdateSkillT(TypedDict):
    skill_category: str
    skill_name: str
    skill_description: str
    skill_level: enum_skill_level

    user_id:str
    id:str

class DeleteSkillT(TypedDict):
    id:str
    user_id:str            


class AvailableTimeT(TypedDict):
    id:str
    skill_id:str
    available_day:str
    start_time:str
    end_time:str
    created_at:str
    updated_at:str
    deleted_at:str

class CreateAvailableTimeT(TypedDict):
    skill_id:str
    available_day:str
    start_time:str
    end_time:str

class UpdateAvailableTimeT(TypedDict):
    skill_id:str
    available_day:enum_available_day    
    start_time:str
    end_time:str
    id:str

class DeleteAvailableTimeT(TypedDict):
    id:str
    skill_id:str
    
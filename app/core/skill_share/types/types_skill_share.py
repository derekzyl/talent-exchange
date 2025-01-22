# Types/Enums
from enum import Enum
from typing import TypedDict, List, Optional
from datetime import datetime

class SkillShareStatusEnum(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ReviewRatingEnum(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

# Type definitions
class SkillShareRequestT(TypedDict):
    id: str
    requester_id: str
    provider_id: str
    requester_skill_id: str
    provider_skill_id: str
    status: SkillShareStatusEnum
    message: str
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

class CreateSkillShareRequestT(TypedDict):
    requester_id: str
    provider_id: str
    requester_skill_id: str
    provider_skill_id: str
    message: str

class OngoingSkillShareT(TypedDict):
    id: str
    skill_share_id: str
    start_date: datetime
    end_date: datetime
    status: SkillShareStatusEnum
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]


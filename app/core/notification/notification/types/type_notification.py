from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, TypedDict

from pydantic import BaseModel


@dataclass
class Notification:
    id: str  # Assuming UUID
    message: str
    subject:str
    is_read:str
    user_id:str
    created_at: datetime
    updated_at: datetime

class NotificationT(TypedDict):
    id: str  # Assuming UUID
    type: str
    message: str
    is_read:str
    user_id:str
    subject:str

    created_at: datetime
    updated_at: datetime



class SendNotificationT(TypedDict):
    subject:str
    data: str
    user_id:str
   

class NotificationTypeE(str, Enum):
    TEXT = "TEXT"
    MIXED = "MIXED"
    IMAGE = "IMAGE"



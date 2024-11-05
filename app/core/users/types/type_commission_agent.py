

from dataclasses import dataclass
from typing import TypedDict


@dataclass
class CommissionAgentD:
    id: int
    name: str
    email: str
    phone: str
    commission_rate: float
    commission_type: str
    commission_id: int
    commission_name: str
    commission_email: str
    commission_phone: str
    commission_rate_type: str
  

class CommissionAgentT(TypedDict):
    id: int
    name: str
    email: str
    phone: str
    commission_rate: float
    commission_type: str
    commission_id: int
    commission_name: str
    commission_email: str
    commission_phone: str
    commission_rate_type: str
  
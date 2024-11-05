from datetime import datetime
from typing import TypedDict


class BusinessSubT(TypedDict):
    id:str
    subscription_id:str
    user_id:str
    business_id:str
    duration:int
    start_date:datetime
    end_date:datetime
    created_at:datetime
    updated_at:datetime
    
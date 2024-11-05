from datetime import datetime
from typing import TypedDict


class SubscriptionT(TypedDict):
    id:str
    products:int
    users:int
    amount:int
    inventory:str
    use_analysis:bool
    sellers:int
    use_ai:bool
    created_at:datetime
    updated_at:datetime
    
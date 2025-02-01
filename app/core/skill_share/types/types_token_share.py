# Updated SkillShare and Token Routes

# types/types_token.py

from typing import Optional, TypedDict
from datetime import datetime

class TokenBalanceT(TypedDict):
    balance: float

class TokenPurchaseT(TypedDict):
    amount: float
    payment_method: str  # e.g., 'credit_card', 'paypal'
    currency: str  # e.g., 'USD', 'EUR'

class TokenTransferT(TypedDict):
    recipient_id: str
    amount: float
    message: Optional[str]|None 


from dataclasses import dataclass


@dataclass
class Wallet:
    id: int
    name: str
    balance: float
    currency: str
    user_id: int
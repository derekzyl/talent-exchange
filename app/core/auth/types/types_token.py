from dataclasses import dataclass

from app.config.config import TokenType


@dataclass
class Token:
    type:TokenType
    user_id:str
    expires:str
    blacklisted:bool 
    created_at:str
    updated_at:str
    
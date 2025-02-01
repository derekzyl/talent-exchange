from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.config.database.db import BaseModelClass
from datetime import datetime

class TokenSkillModel(BaseModelClass):
    __tablename__ = "SKILL_TOKENS"

    user_id: Mapped[str] = mapped_column(ForeignKey("USER.id"))
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Relationships
    user = relationship("UserModel", foreign_keys=[user_id])
    transactions = relationship("TokenSkillTransactionModel", back_populates="token")

class TokenSkillTransactionModel(BaseModelClass):
    __tablename__ = "SKILL_TOKEN_TRANSACTIONS"

    token_id: Mapped[str] = mapped_column(ForeignKey("SKILL_TOKENS.id"))
    skill_share_request_id: Mapped[str] = mapped_column(ForeignKey("SKILL_SHARE_REQUESTS.id"))
    amount: Mapped[float] = mapped_column(Float)
    transaction_type: Mapped[str] = mapped_column(String)  # 'DEBIT' or 'CREDIT'
    
    # Relationships
    token = relationship("TokenSkillModel", back_populates="transactions")
    skill_share_request = relationship("SkillShareRequestModel", foreign_keys=[skill_share_request_id] )

# Models
from sqlalchemy import Column, ForeignKey, String, Enum, DateTime, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.config.database.db import BaseModelClass
from app.core.skill_share.types.types_skill_share import SkillShareStatusEnum

class SkillShareRequestModel(BaseModelClass):
    __tablename__ = "SKILL_SHARE_REQUESTS"

    requester_id: Mapped[str] = mapped_column(ForeignKey("USER.id"))
    provider_id: Mapped[str] = mapped_column(ForeignKey("USER.id"))
    requester_skill_id: Mapped[str] = mapped_column(ForeignKey("SKILLS.id"), nullable=True)
    provider_skill_id: Mapped[str] = mapped_column(ForeignKey("SKILLS.id"))
    status = mapped_column(String, default=SkillShareStatusEnum.PENDING.value)
    message = mapped_column(Text, nullable=True)

    # Relationships
    requester = relationship("UserModel", foreign_keys=[requester_id])
    provider = relationship("UserModel", foreign_keys=[provider_id])
    requester_skill = relationship("SkillModel", foreign_keys=[requester_skill_id])
    provider_skill = relationship("SkillModel", foreign_keys=[provider_skill_id])
    ongoing_share = relationship("OngoingSkillShareModel", back_populates="skill_share")
    reviews = relationship("ReviewModel", back_populates="skill_share")

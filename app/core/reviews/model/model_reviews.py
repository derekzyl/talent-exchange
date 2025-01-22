
# Models
from sqlalchemy import Column, ForeignKey, String, Enum, DateTime, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.config.database.db import BaseModelClass
from app.core.skill_share.types.types_skill_share import SkillShareStatusEnum
class ReviewModel(BaseModelClass):
    __tablename__ = "REVIEWS"

    reviewer_id: Mapped[str] = mapped_column(ForeignKey("USER.id"))
    reviewee_id: Mapped[str] = mapped_column(ForeignKey("USER.id"))
    skill_share_id: Mapped[str] = mapped_column(ForeignKey("SKILL_SHARE_REQUESTS.id"))
    rating = mapped_column(String)
    comment = mapped_column(Text, nullable=True)

    # Relationships
    reviewer = relationship("UserModel", foreign_keys=[reviewer_id])
    reviewee = relationship("UserModel", foreign_keys=[reviewee_id])


    skill_share = relationship("SkillShareRequestModel", back_populates="reviews")

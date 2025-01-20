

from sqlalchemy import Boolean, Column, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database.db import BaseModelClass


class SkillAvailableTimeModel(BaseModelClass):
    __tablename__ = "SKILL_AVAILABLE_TIME"


    available_day = mapped_column(String(255), nullable=False)
    start_time = mapped_column(String(255), nullable=False)
    end_time = mapped_column(String(255), nullable=False)

    # foreignkey 
    skill_id: Mapped[str] = mapped_column(ForeignKey("SKILLS.id"))

    # relationship
    skill_available_time__skill = relationship("SkillModel", back_populates="skill__skill_available_time")
    



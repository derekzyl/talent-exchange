

from sqlalchemy import Boolean, Column, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database.db import BaseModelClass


class SkillModel(BaseModelClass):
    __tablename__ = "SKILLS"


    skill_category = mapped_column(String(255), nullable=False)
    skill_name = mapped_column(String(255), nullable=False)
    skill_level = mapped_column(String(255), nullable=False)
    skill_description = mapped_column(String(255), nullable=False)
    

    # foreign key 
    user_id: Mapped[str] = mapped_column(ForeignKey("USER.id"))


    # relationship
    skill__user = relationship("UserModel", back_populates="user__skill")
    skill__skill_available_time = relationship("SkillAvailableTimeModel", back_populates="skill_available_time__skill")
    
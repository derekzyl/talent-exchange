
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database.db import Base, BaseModelClass, TimeStamp
from app.core.users.types.type_user import GenderE
from app.utils.uuid_generator import id_gen

if TYPE_CHECKING:
    from app.core.auth.models.model_token import TokenModel
    

class UserModel(BaseModelClass):
    __tablename__ = "USER"
    
    first_name:Mapped[str]
    last_name:Mapped[str]
    username:Mapped[str]= mapped_column(String(255), nullable=True, unique=True)
    password:Mapped[str] =mapped_column(String(255), nullable=False)
    email:Mapped[str]= mapped_column(String(255), unique=True, nullable=False)
    phone:Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    language:Mapped[str]= mapped_column(String(255), unique=True, nullable=True)
    country:Mapped[str]= mapped_column(String(255), nullable=True)
    region:Mapped[str]= mapped_column(String(255), nullable=True)

    
    gender:Mapped[str]=mapped_column(Enum(GenderE), nullable=True)

    allow_login:Mapped[bool] = mapped_column(Boolean, default=True)
    
  

    # foreign keys
    # business_id:Mapped[str] = mapped_column(String(255), ForeignKey("BUSINESS.id"))

    #relationship
    # user__business:Mapped["BusinessModel"] = relationship(back_populates="business__user")
    user__token:Mapped["TokenModel"] = relationship(back_populates="token__user")
    user__notification= relationship("NotificationModel",back_populates="notification__user")
    user__skill= relationship("SkillModel", back_populates="skill__user")



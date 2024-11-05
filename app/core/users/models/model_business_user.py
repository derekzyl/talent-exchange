
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (ARRAY, DATETIME, INTEGER, Boolean, DateTime, Enum,
                        Float, ForeignKey, Integer, String)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database.db import Base, TimeStamp
from app.core import business
from app.core.users.types.type_business_user import UserTypeE
from app.core.users.types.type_user import GenderE
from app.utils.uuid_generator import id_gen

if TYPE_CHECKING:
    from app.core.auth.models.model_token import TokenModel
    from app.core.business.models.model_business import BusinessModel

class UserBusinessModel(Base, TimeStamp):
    __tablename__ = "USER_BUSINESS"
    id:Mapped[str] = mapped_column(
        String(255), primary_key=True, default=id_gen() , unique=True
    )
    first_name:Mapped[str]
    last_name:Mapped[str]
    password:Mapped[str] =mapped_column(String(255), nullable=False)
    email:Mapped[str]= mapped_column(String(255), unique=True, nullable=False)
    phone:Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    language:Mapped[str]
    gender:Mapped[str]=mapped_column(Enum(GenderE))
    user_type:Mapped[str] = mapped_column(Enum(UserTypeE))
    allow_login:Mapped[bool] = mapped_column(Boolean, default=True)
    is_commission_agent:Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_At:Mapped[datetime]

    # foreign keys
    # business_id:Mapped[str] = mapped_column(String(255), ForeignKey("BUSINESS.id"))

    #relationship
    # user__business:Mapped["BusinessModel"] = relationship(back_populates="business__user")
    user__token:Mapped["TokenModel"] = relationship(back_populates="token__user")



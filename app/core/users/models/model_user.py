
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database.db import Base, TimeStamp
from app.core.users.types.type_user import GenderE
from app.utils.uuid_generator import id_gen

if TYPE_CHECKING:
    from app.core.auth.models.model_token import TokenModel

class UserModel(Base, TimeStamp):
    __tablename__ = "USER"
    id:Mapped[str] = mapped_column(
        String(255), primary_key=True, default=id_gen() , unique=True
    )
    first_name:Mapped[str]
    last_name:Mapped[str]
    username:Mapped[str]= mapped_column(String(255), nullable=True, unique=True)
    password:Mapped[str] =mapped_column(String(255), nullable=False)
    email:Mapped[str]= mapped_column(String(255), unique=True, nullable=False)
    phone:Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    language:Mapped[str]= mapped_column(String(255), unique=True, nullable=True)
    gender:Mapped[str]=mapped_column(Enum(GenderE), nullable=True)

    allow_login:Mapped[bool] = mapped_column(Boolean, default=True)
    
    deleted_At:Mapped[datetime]= mapped_column(DateTime, unique=True, nullable=True)

    # foreign keys
    # business_id:Mapped[str] = mapped_column(String(255), ForeignKey("BUSINESS.id"))

    #relationship
    # user__business:Mapped["BusinessModel"] = relationship(back_populates="business__user")
    user__token:Mapped["TokenModel"] = relationship(back_populates="token__user")



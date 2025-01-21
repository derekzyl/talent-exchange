
from typing import TYPE_CHECKING

from sqlalchemy import (ARRAY, DATETIME, INTEGER, Boolean, DateTime, Enum,
                        Float, ForeignKey, Integer, String)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.config import TokenType
from app.config.database.db import Base, BaseModelClass, TimeStamp
from app.utils.uuid_generator import id_gen

if TYPE_CHECKING:
    from app.core.users.models.model_user import UserModel


class   TokenModel(BaseModelClass):
    __tablename__="TOKEN"
    
    type:Mapped[str] = mapped_column(String, nullable=False )
    expires:Mapped[str] = mapped_column(DateTime, nullable=False)
    blacklisted:Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    token:Mapped[str] = mapped_column(String, nullable=False)

    #foreign keys
    user_id:Mapped[str] = mapped_column(String, ForeignKey("USER.id"))
    
    
    #relationships
    token__user:Mapped["UserModel"] = relationship(back_populates="user__token")
    
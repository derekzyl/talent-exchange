
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database.db import Base, BaseModelClass, TimeStamp
from app.core.users.types.type_user import GenderE
from app.utils.uuid_generator import id_gen
class OngoingSkillShareModel(BaseModelClass):
    __tablename__ = "ONGOING_SKILL_SHARES"

    skill_share_id: Mapped[str] = mapped_column(ForeignKey("SKILL_SHARE_REQUESTS.id"))
    start_date = mapped_column(DateTime, nullable=False)
    end_date = mapped_column(DateTime, nullable=False)
    status = mapped_column(String)
    notes = mapped_column(Text, nullable=True)

    # Relationships
    skill_share = relationship("SkillShareRequestModel", back_populates="ongoing_share")

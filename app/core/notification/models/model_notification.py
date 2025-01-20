from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database.db import Base, BaseModelClass, TimeStamp
from app.core.notification.types.type_notification import NotificationTypeE
from app.utils.uuid_generator import id_gen



# from modules.auth.model.model import UserModel




# The `NotificationModel` class is a subclass of the `Base` class and inherits from the `Base` class.
# This class likely represents a notification model that inherits from a base class and includes
# timestamp functionality.
class NotificationModel(BaseModelClass):

    __tablename__: str = "NOTIFICATION"

    message: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[NotificationTypeE] = mapped_column(Enum(NotificationTypeE))
    subject:Mapped[str] = mapped_column(nullable=True)

    is_read: Mapped[bool] = mapped_column(default=False)


    #foreign key
    user_id: Mapped[str] = mapped_column(ForeignKey("USER.id"))

    #relationship
    notification__user= relationship("UserModel", back_populates="user__notification"  )


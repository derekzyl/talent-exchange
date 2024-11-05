import random
import string
import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.db import Base

if TYPE_CHECKING:
    from modules.job.models.job_approved_mavens_model import ApprovedMavenModel
    from utils.notifications.model.notification_model import NotificationModel

from utils.uuid_generator import id_uuid


# The UserModel class is a subclass of the Base class.
class UserModel(Base):

    """USER Model

    This class is used to represent a user in the database. It contains the following attributes:



    The `id` attribute is a mapped column of type `String` with a default value of `id_uuid()`.
    The `email` attribute is a mapped column of type `String` with a unique constraint.
    The `username` attribute is a mapped column of type `String` with a unique constraint.
    The `location` attribute is a mapped column of type `JSONB` with a default value of `{}`.
    The `password` attribute is a mapped column of type `String`.
    The `is_email_verified` attribute is a mapped column of type `Boolean` with a default value of `False`.
    """

    # The `__tablename__` attribute is used to specify the name of the database table that will be
    # created for the `UserModel` class. In this case, the table name is set to "USER".
    __tablename__ = "USER"

    id: Mapped[str] = mapped_column(String, default=id_uuid(), primary_key=True)

    email: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    location: Mapped[dict] = mapped_column(
        JSONB, default={}
    )  # the location has the coordinates latitude and longitude

    password: Mapped[str] = mapped_column(String)
    is_email_verified: Mapped[str] = mapped_column(Boolean, default=False)
    token: Mapped[str] = mapped_column(String, default="")
    token_expiry_time: Mapped[str] = mapped_column(DateTime, default=datetime.now())

    role: Mapped[str] = mapped_column(String, default="USER")
    created_at: Mapped[date] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[date] = mapped_column(DateTime, default=datetime.now())

    # The comment `# the receiver model relationship spinning` is indicating that the code is defining
    # a relationship between the `UserModel` and the `NotificationModel` classes. Specifically, it is
    # defining a one-to-many relationship where a user can have multiple notifications as a receiver.
    # This relationship is established through the `receiver___notification` attribute in the
    # `UserModel` class, which is a mapped column representing the relationship. The `back_populates`
    # parameter is used to specify the corresponding attribute in the `NotificationModel` class that
    # represents the inverse relationship.
    # the receiver model relationship spinning
    receiver___notification: Mapped["NotificationModel"] = relationship(
        "NotificationModel",
        back_populates="notification___receiver",
        cascade="all, delete",
        passive_deletes=True,
    )
    sender___notification: Mapped["NotificationModel"] = relationship(
        "NotificationModel",
        back_populates="notification___sender",
        cascade="all, delete",
        passive_deletes=True,
    )

    user___approved_maven: Mapped["ApprovedMavenModel"] = relationship(
        back_populates="approved_maven___user",
        cascade="all, delete",
        passive_deletes=True,
    )

    # user_job_maven = relationship("JobModel", back_populates="job_user_maven")
    # user_job_client = relationship("JobModel", back_populates="job_user_client")

    # user_proposal = relationship("ProposalModel", back_populates="proposal_user")
    # user_contract = relationship("ContractModel", back_populates="contract_user")
    # user___client_rating = relationship(
    #     "ClientRatingModel", back_populates="client_rating___user"
    # )
    # user___maven_rating = relationship(
    #     "MavenRatingModel", back_populates="maven_rating___user"
    # )
    # user_message = relationship("MessageModel", back_populates="message_user")
    # user_dialogue = relationship("DialogueModel", back_populates="dialogue_user")

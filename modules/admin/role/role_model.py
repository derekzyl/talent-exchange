from datetime import datetime
from os import name
from sqlalchemy import Column, Date, String, ARRAY
from server.db import Base
from utils.uuid_generator import id_uuid


class RoleModel(Base):
    __tablename__ = "ROLE"
    id = Column(String, primary_key=True, default=id_uuid())
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    permission = Column(ARRAY(String))
    created_at = Column(Date, nullable=False, default=datetime.utcnow())

    updated_at = Column(Date, nullable=False, default=datetime.utcnow())

    created_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=False)

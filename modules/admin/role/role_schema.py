from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Date

from modules.general_crud.crud_schema import PermissionE


class RoleSchema(BaseModel):
    name: str
    description: Optional[str]
    permissions: list[PermissionE]


class RoleSchemaInDb(RoleSchema):
    id: str
    created_at: Date
    updated_at: Date
    created_by: str
    updated_by: str

    class Config:
        orm_mode = True

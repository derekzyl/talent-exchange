from fastapi import HTTPException, status
from modules.admin.role.role_schema import RoleSchema
from modules.auth.schema.schema import UserInDbSchema
from sqlalchemy.orm import Session


class RoleFactory:
    def __init__(self):
        pass

    async def createRole(
        self, database: Session, role_data: RoleSchema, user: UserInDbSchema
    ):
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

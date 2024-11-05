from enum import Enum
from pydantic import BaseModel, Extra


class QuerySchema(BaseModel):
    skips: int | None
    limits: int | None
    filters_by: dict | None
    page: int | None
    sort_by: str | None

    class config:
        extra = Extra.allow


class PermissionE(str, Enum):
    # create a user
    CREATE_USER = "CREATE_USER"
    READ_USER = "READ_USER"
    UPDATE_USER = "UPDATE_USER"
    DELETE_USER = "DELETE_USER"
    # create a staff
    CREATE_JOB = "CREATE_JOB"
    READ_JOB = "READ_JOB"
    UPDATE_JOB = "UPDATE_JOB"
    DELETE_JOB = "DELETE_JOB"

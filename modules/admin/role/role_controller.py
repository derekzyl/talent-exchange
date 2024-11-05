from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from modules.admin.role.role_schema import RoleSchema
from modules.auth.controller.controller import protector
from server.db import get_db


roleRouter: APIRouter = APIRouter(prefix="/role")


@roleRouter.post("/create")
async def createRole(
    db: Session = Depends(get_db),
    user=Depends(protector),
    role: RoleSchema = Body(...),
):
    pass


async def getOneRole():
    pass


async def getManyRole():
    pass


async def updateRole():
    pass


async def deleteRole():
    pass

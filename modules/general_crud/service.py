from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from server.db import Base

Model = TypeVar(name="Model", bound=Base)  # type:ignore
DbSchema = TypeVar(name="DbSchema", bound=BaseModel)
CreateSchema = TypeVar(name="CreateSchema", bound=BaseModel)


def createService(
    db: Session, model: type[Model], schema: dict, exempt: str | None = None
):
    db_obj = model(**schema)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    if exempt:
        select_data = db.execute(select(model))
    return db_obj


def getService(db: Session, model: type[Model], id: str):
    return db.query(model).filter(model.id == id).first()


def getServices(db: Session, model: type[Model], skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()


def updateService(db: Session, model: type[Model], id: str, schema: DbSchema):
    db_obj = db.query(model).filter(model["id"] == id)
    db_obj.update(dict(schema.model_dump()))
    db.commit()
    db.refresh(db_obj)
    return db_obj

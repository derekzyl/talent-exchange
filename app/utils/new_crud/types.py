from typing import Type, TypeVar

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Define type variables
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

Base = declarative_base()


def _get_sqlalchemy_type(type_name: str) -> Type:
    """Convert string type names to SQLAlchemy types"""
    type_mapping = {
        'string': String,
        'integer': Integer,
        'boolean': Boolean,
        'datetime': DateTime,
    }
    return type_mapping.get(type_name.lower(), String)

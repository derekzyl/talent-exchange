from typing import Generic, TypeVar, Type, Optional, List, Any, Dict, Union
from fastapi import FastAPI, HTTPException, Query, Request, Response
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, joinedload
from pydantic import BaseModel, create_model
from datetime import datetime
from fastapi.responses import JSONResponse
import math

# Define type variables
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

Base = declarative_base()



def create_api_router(
    model: Type[ModelType],
    create_schema: Type[CreateSchemaType],
    update_schema: Type[UpdateSchemaType],
    prefix: str
) -> FastAPI:
    """Create FastAPI router with CRUD endpoints for a model"""
    router = FastAPI()
    crud_service = CRUDService(model)

    @router.post(f"/{prefix}", response_model=model)
    async def create(request: Request, obj_in: create_schema, db: Session):
        """Create a new record"""
        return await crud_service.create(db, obj_in=obj_in)

    @router.post(f"/{prefix}/bulk", response_model=List[model])
    async def create_many(request: Request, obj_list: List[create_schema], db: Session):
        """Create multiple records"""
        return await crud_service.create_many(db, obj_list=obj_list)

    @router.put(f"/{prefix}", response_model=model)
    async def update(request: Request, obj_in: update_schema, filter_query: Dict[str, Any], db: Session):
        """Update a record"""
        return await crud_service.update(db, filter_query=filter_query, obj_in=obj_in)

    @router.get(f"/{prefix}", response_model=Dict[str, Any])
    async def get_many(
        request: Request,
        db: Session,
        skip: int = Query(0),
        limit: int = Query(100),
        filter_query: Dict[str, Any] = None,
        populate: List[str] = Query(None)
    ):
        """Get multiple records"""
        return await crud_service.get_many(
            db,
            filter_query=filter_query,
            skip=skip,
            limit=limit,
            populate=populate
        )

    @router.delete(f"/{prefix}")
    async def delete(request: Request, filter_query: Dict[str, Any], db: Session):
        """Delete a record"""
        return await crud_service.delete(db, filter_query=filter_query)

    @router.delete(f"/{prefix}/bulk")
    async def delete_many(request: Request, filter_query: Dict[str, Any], db: Session):
        """Delete multiple records"""
        return await crud_service.delete_many(db, filter_query=filter_query)

    @router.get(f"/{prefix}/one", response_model=model)
    async def get_one(
        request: Request,
        filter_query: Dict[str, Any],
        populate: List[str] = Query(None),
        db: Session
    ):
        """Get a single record"""
        return await crud_service.get_one(
            db,
            filter_query=filter_query,
            populate=populate
        )

    return router

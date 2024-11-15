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

class CRUDService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    CRUD service class that provides create, read, update, and delete operations
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, db: Session, *, obj_in: CreateSchemaType, check_filter: Dict = None) -> ModelType:
        """Create a new record"""
        if check_filter:
            existing = db.query(self.model).filter_by(**check_filter).first()
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Data for {', '.join(check_filter.keys())} already exists"
                )

        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def create_many(
        self, 
        db: Session, 
        *, 
        obj_list: List[CreateSchemaType],
        check_filters: List[Dict] =[]
    ) -> List[ModelType]:
        """Create multiple records"""
        if check_filters:
            for check in check_filters:
                existing = db.query(self.model).filter_by(**check).first()
                if existing:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Data for {', '.join(check.keys())} already exists"
                    )

        db_objs = []
        for obj_in in obj_list:
            obj_in_data = obj_in.dict()
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db_objs.append(db_obj)

        db.commit()
        for obj in db_objs:
            db.refresh(obj)
        return db_objs

    async def update(
        self,
        db: Session,
        *,
        filter_query: Dict[str, Any],
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Optional[ModelType]:
        """Update a record"""
        db_obj = db.query(self.model).filter_by(**filter_query).first()
        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} not found"
            )

        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def get_many(
        self,
        db: Session,
        *,
        filter_query: Dict[str, Any] = {},
        skip: int = 0,
        limit: int = 100,
        order_by: str|None = None,
        populate: List[str] = []
    ) -> List[ModelType]:
        """Get multiple records with pagination and filtering"""
        query = db.query(self.model)

        if filter_query:
            query = query.filter_by(**filter_query)

        if populate:
            for relation in populate:
                query = query.options(joinedload(getattr(self.model, relation)))

        if order_by:
            if order_by.startswith("-"):
                query = query.order_by(getattr(self.model, order_by[1:]).desc())
            else:
                query = query.order_by(getattr(self.model, order_by))

        total = query.count()
        items = query.offset(skip).limit(limit).all()

        return {
            "items": items,
            "total": total,
            "page": math.ceil(skip / limit) + 1,
            "pages": math.ceil(total / limit)
        }

    async def delete(self, db: Session, *, filter_query: Dict[str, Any]) -> bool:
        """Delete a record"""
        obj = db.query(self.model).filter_by(**filter_query).first()
        if not obj:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} not found"
            )
        
        db.delete(obj)
        db.commit()
        return True

    async def delete_many(self, db: Session, *, filter_query: Dict[str, Any]) -> bool:
        """Delete multiple records"""
        result = db.query(self.model).filter_by(**filter_query).delete()
        db.commit()
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"No {self.model.__name__} records found to delete"
            )
        return True

    async def get_one(
        self,
        db: Session,
        *,
        filter_query: Dict[str, Any],
        populate: List[str] = None
    ) -> Optional[ModelType]:
        """Get a single record"""
        query = db.query(self.model)

        if populate:
            for relation in populate:
                query = query.options(joinedload(getattr(self.model, relation)))

        obj = query.filter_by(**filter_query).first()
        if not obj:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} not found"
            )
        return obj

class Queries:
    """Query helper class for handling filtering, sorting, and pagination"""
    def __init__(self, query: Any, request_query: Dict[str, Any]):
        self.query = query
        self.request_query = request_query

    def filter(self):
        """Apply filters from query parameters"""
        filter_params = {}
        excluded_fields = ["page", "sort", "limit", "fields"]
        
        for key, value in self.request_query.items():
            if key not in excluded_fields:
                if "__" in key:
                    field, operator = key.split("__")
                    if operator == "gte":
                        filter_params[field] >= value
                    elif operator == "gt":
                        filter_params[field] > value
                    elif operator == "lte":
                        filter_params[field] <= value
                    elif operator == "lt":
                        filter_params[field] < value
                else:
                    filter_params[key] = value
        
        self.query = self.query.filter_by(**filter_params)
        return self

    def sort(self):
        """Apply sorting"""
        if self.request_query.get("sort"):
            sort_fields = self.request_query["sort"].split(",")
            for field in sort_fields:
                if field.startswith("-"):
                    self.query = self.query.order_by(getattr(self.model, field[1:]).desc())
                else:
                    self.query = self.query.order_by(getattr(self.model, field))
        else:
            self.query = self.query.order_by(self.model.created_at.desc())
        return self

    def paginate(self):
        """Apply pagination"""
        page = int(self.request_query.get("page", 1))
        limit = int(self.request_query.get("limit", 100))
        skip = (page - 1) * limit
        self.query = self.query.offset(skip).limit(limit)
        return self

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

def generate_dynamic_model(
    name: str,
    fields: Dict[str, Any],
    base: Type = Base
) -> Type[ModelType]:
    """Generate SQLAlchemy model dynamically"""
    attrs = {
        '__tablename__': name.lower(),
        'id': Column(Integer, primary_key=True, index=True),
        'created_at': Column(DateTime, default=datetime.utcnow),
        'updated_at': Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    }

    for field_name, field_type in fields.items():
        if isinstance(field_type, dict):
            if field_type.get('type') == 'relationship':
                attrs[field_name] = relationship(
                    field_type['model'],
                    backref=field_type.get('backref'),
                    lazy=field_type.get('lazy', 'select')
                )
            else:
                attrs[field_name] = Column(
                    _get_sqlalchemy_type(field_type['type']),
                    **{k: v for k, v in field_type.items() if k != 'type'}
                )
        else:
            attrs[field_name] = Column(_get_sqlalchemy_type(field_type))

    return type(name, (base,), attrs)

def _get_sqlalchemy_type(type_name: str) -> Type:
    """Convert string type names to SQLAlchemy types"""
    type_mapping = {
        'string': String,
        'integer': Integer,
        'boolean': Boolean,
        'datetime': DateTime,
    }
    return type_mapping.get(type_name.lower(), String)

def create_response_message(
    success: bool,
    message: str,
    data: Any = None,
    doc_length: int = None,
    error: Any = None,
    stack: Any = None,
    config: str = "production"
) -> Dict[str, Any]:
    """Create standardized response message"""
    if success:
        response = {
            "message": message,
            "data": data,
            "success": success
        }
        if doc_length is not None:
            response["doc_length"] = doc_length
        return response
    else:
        response = {
            "message": message,
            "error": error,
            "success": success
        }
        if config == "development" and stack:
            response["stack"] = stack
        return response
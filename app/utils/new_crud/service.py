import math
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, joinedload

from app.utils.new_crud.queries import NewQueries

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

    async def create(self, db: Session, *, obj_in: CreateSchemaType, check_filter: dict = None) -> ModelType:
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
        check_filters: List[Dict]|None = None
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
        filter_query: Dict[str, Any]|None = None,
        query_params: Dict[str, Any] |None = None,
        
        skip: int = 0,
        limit: int = 100,
        order_by: str|None = None,
        populate: List[str]|None = None
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
        q =NewQueries(query, query_params)
        qu = q.filter().sort().paginate().query.all()

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


from typing import Any, Dict, List, Optional
from sqlalchemy import select  
from fastapi import HTTPException, status
from sqlalchemy import delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.future import select as sa_select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import insert

from app.utils.crud.types_crud import ResponseMessage, response_message
from app.utils.logger import log

from .queries import Queries


class CrudService:
    # def __init__(self, model: DeclarativeMeta, db: AsyncSession):
    def __init__(self, model: DeclarativeMeta, db: AsyncSession):
        self.model = model
        self.db = db

    async def get_many(
        self,
        query: Dict[str, Any],
        filter: Optional[Dict[str, Any]] = None,
        select_fields: Optional[List[str]] = None
    ) -> ResponseMessage:
        query_model = sa_select(self.model) # type: ignore
        try:
            if filter:
                for key, value in filter.items():
                    query_model = query_model.where(getattr(self.model, key) == value)

            query_handler = Queries(query_model, query)

            # Apply select fields if provided
            if select_fields:
                query_handler.model = query_handler.model.with_only_columns(*[getattr(self.model, field) for field in select]) # type: ignore

            query_handler.filter().limit_fields().paginate().sort()

            results = (await self.db.execute(query_handler.model)).scalars().all()

            if not results:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=response_message(data=None, error="Data not found", message="Data not found", success_status=False)
                )

            return response_message(
                success_status=True,
                message="Data fetched successfully",
                data=results,
                doc_length=len(results)
            )
        except Exception as e:
            log.logs.error(f"Error fetching data: {e}")
            return response_message(
                data=None,
                doc_length=0,
                error=str(e),
                message="Error fetching data",
                success_status=False
            )


    async def get_one(self, data: Dict[str, Any], select: Optional[List[str]] = None) -> ResponseMessage:
        """
        This async function `get_one` retrieves data based on the provided parameters and returns a
        response message.
        
        :param data: The `data` parameter in the function `get_one` is a dictionary that contains
        key-value pairs of information needed to retrieve a specific item. It likely includes the
        necessary data to identify and fetch the item from a data source or database
        :type data: Dict[str, Any]
        :param select: The `select` parameter in the function `get_one` is an optional parameter of type
        List[str]. It is used to specify which fields or columns from the data dictionary should be
        selected or returned in the response. If `select` is not provided, all fields will be returned
        :type select: Optional[List[str]]
        """
  
        
        query = sa_select(self.model).filter_by(**data)  # Ensure this is the correct select function

        
        if select:
            include_fields = [field for field in select if not field.startswith('-')]
            exclude_fields = [field[1:] for field in select if field.startswith('-')]

            # Construct the selected query based on included or excluded fields
            if include_fields:
                fields_to_select = [getattr(self.model, field) for field in include_fields]
            else:
                all_fields = set(self.model.__table__.columns.keys())  # type: ignore
                fields_to_select = [getattr(self.model, field) for field in all_fields if field not in exclude_fields]

            # Query the database for the created item with the selected fields
            query = sa_select(*fields_to_select).filter_by(**data)
           

    
        
        try:
            result = await self.db.execute(query)
          
            db_item_selected = result.fetchone()
         
        except Exception as e:
            log.logs.error(f"Error executing query: {e}")
            return response_message(data=None, doc_length=0, error=str(e), message="Error fetching data", success_status=False)
        
        if db_item_selected is None:
            return response_message(data=None, doc_length=0, error="No data found", message="No data found", success_status=False)
        
        return response_message(data=db_item_selected, doc_length=1, error=None, message="Data fetched successfully", success_status=True)   #     self.db.add(db_item)
    #     await self.db.commit()
    #     await self.db.refresh(db_item)
    #     return response_message(data=db_item, doc_length=1, error=None, message="Data created successfully", success_status=True)
    async def create(self, data: Dict[str, Any], check: Dict[str, Any]|None =None, select: List[str]|None =None):
        """
        This Python async function `create` takes in data, an optional check dictionary, and an optional
        list of select fields.
        
        :param data: A dictionary containing the data to be used for creating a new entry or record
        :type data: Dict[str, Any]
        :param check: The `check` parameter in the `create` method is a dictionary that allows you to
        specify conditions that must be met before creating the data. If the `check` parameter is
        provided, the method will verify that the data meets the conditions specified in the `check`
        dictionary before proceeding with the creation
        :type check: Dict[str, Any]|None
        :param select: The `select` parameter in the `create` method is a list of strings that specifies
        which fields you want to select from the data when creating a new object. If `select` is
        provided, only the fields specified in the list will be included in the operation. If `select`
        is not
        :type select: List[str]|None
        """
        # Check if the data already exists
        if check:
            query = sa_select(self.model).filter_by(**check)
            result = await self.db.execute(query)
            existing_item = result.scalars().first()
            if existing_item:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"The data for: {', '.join(check.keys())} already exists in the database"
                )

        # Create a new record
        db_item = self.model(**data)
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)

        # Handle the select fields
        if select:
            include_fields = [field for field in select if not field.startswith('-')]
            exclude_fields = [field[1:] for field in select if field.startswith('-')]

            # Construct the selected query based on included or excluded fields
            if include_fields:
                fields_to_select = [getattr(self.model, field) for field in include_fields]
            else:
                all_fields = set(self.model.__table__.columns.keys()) # type: ignore
                fields_to_select = [getattr(self.model, field) for field in all_fields if field not in exclude_fields]

            # Query the database for the created item with the selected fields
            query = sa_select(*fields_to_select).filter_by(id=db_item.id)
            result = await self.db.execute(query)
            db_item_selected = result.fetchone()
    

            # Convert the selected fields into a dictionary
            if db_item_selected:
                db_item_dict = db_item_selected
            else:
                db_item_dict = None
        else:
            db_item_dict = db_item
        log.logs.info(f"db Selected fields: {db_item_dict}")

        return response_message(
            data=db_item_dict,
            doc_length=1,
            error=None,
            message="Data created successfully",
            success_status=True
        )

    async def update(self, filter: dict[str, Any], data: Dict[str, Any]):
        query = update(self.model).filter_by(**filter). values(**data, updated_at=func.now()).execution_options(synchronize_session="fetch")
        await self.db.execute(query)
        await self.db.commit()

        updated_item = await self.get_one(**filter)
        if updated_item:
            return response_message(data=updated_item, doc_length=1, error=None, message="Data updated successfully", success_status=True)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response_message(data=None, error="Data not found", message="Data not found", success_status=False)
        )

    async def delete(self, filter: dict[str, Any]):
        query = delete(self.model).filter_by(**filter).execution_options(synchronize_session="fetch")
        result = await self.db.execute(query)
        await self.db.commit()

        if result.rowcount > 0:
            return response_message(data=None, error=None, message="Data deleted successfully", success_status=True)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response_message(data=None, error="Data not found", message="Data not found", success_status=False)
        )

    async def _include_fields(self, field: str) -> Any:
        return getattr(self.model, field, None)

    async def _exclude_fields(self, field: str) -> Any:
        return getattr(self.model, field, None)


    async def create_many(self, data: List[Dict[str, Any]], check: List[Dict[str, Any]] | None = None):
        """
        This method creates multiple records in the database from a list of dictionaries.

        :param data: A list of dictionaries, each representing a record to be created.
        :type data: List[Dict[str, Any]]
        :param check: Optional. A list of dictionaries for ensuring no duplicates exist before insertion.
        :type check: List[Dict[str, Any]] | None
        :return: A response message with the results of the bulk insert.
        """
        try:
            if check:
                for condition in check:
                    query = sa_select(self.model).filter_by(**condition)
                    result = await self.db.execute(query)
                    if result.scalars().first():
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The data for: {', '.join(condition.keys())} already exists in the database"
                        )

            # Perform a bulk insert
            query = insert(self.model).values(data)
            await self.db.execute(query)
            await self.db.commit()

            return response_message(
                data=data,
                doc_length=len(data),
                error=None,
                message="Bulk data created successfully",
                success_status=True
            )
        except IntegrityError as e:
            log.logs.error(f"IntegrityError during bulk insert: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {str(e)}"
            )
        except Exception as e:
            log.logs.error(f"Error creating bulk data: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred: {str(e)}"
            )

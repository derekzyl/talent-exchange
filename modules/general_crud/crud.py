from typing import Any, Generic, Type, TypeVar

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session, exc

from modules.general_crud.query import Query
from server.db import Base
from utils.response_message import responseMessage

Model = TypeVar(name="Model", bound=Base)  # type:ignore
DbSchema = TypeVar(name="DbSchema", bound=BaseModel)
CreateSchema = TypeVar(name="CreateSchema", bound=BaseModel)


# The CRUD class is a generic class that provides basic CRUD (Create, Read, Update, Delete) operations
# for a given model and database schema.


class CRUD(Generic[Model, DbSchema]):

    """_summary_"""

    def __init__(self, model: Type[Model], schema: Type[DbSchema], db: Session):
        """
        The function initializes an object with a model, schema, and database session.

        Args:
          model (Type[Model]): The `model` parameter is of type `Type[Model]`. It represents the model
        class that is used to interact with the database. This class should be a subclass of the `Model`
        class.
          schema (Type[DbSchema]): The `schema` parameter is a type hint that specifies the type of the
        database schema. It is expected to be a subclass of `DbSchema`.
          db (Session): The `db` parameter is of type `Session`. It represents a database session, which
        is used to interact with the database. It is typically created using a database connection and
        is responsible for managing transactions and executing database queries.
        """
        self.model = model
        self.schema = schema
        self.db: Session = db

    def create(self, create_data: Any):
        """create in crud schema

        Args:
            create_data (type[CreateSchema]): it receives a create data schema wrapped in a pydantic object

        Raises:
            HTTPException: sqlalchemy error
            HTTPException: any other error

        Returns:
            _type_: a created data
        """
        data_json = jsonable_encoder(create_data)
        my_model = self.model(**data_json)  # type:ignore
        try:
            self.db.add(my_model)
            self.db.commit()
            self.db.refresh(my_model)
            return my_model
        except exc.sa_exc.SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=responseMessage(
                    {
                        "data": {"error": e},
                        "message": "sqlalchemy error occurred",
                        "success_status": False,
                    }
                ),
            )
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=responseMessage(
                    {
                        "data": {
                            "error": f"error is coming from database creation",
                        },
                        "message": "creating  failed",
                        "success_status": False,
                    }
                ),
            )

    def getOne(self, id: str):
        """
        The function `getOne` retrieves a single record from the database based on the provided `id`.

        Args:
          id (str): The "id" parameter is a string that represents the unique identifier of the object
        you want to retrieve from the database.

        Returns:
          the result of a database query for a specific record with the given ID.
        """
        getOne = (
            self.db.query(self.model).filter(self.model.id == id).first()  # type: ignore
        )  # type:ignore
        return getOne

    def getMany(self, query_param: dict):
        """
        The function `getMany` retrieves multiple records from a database based on the provided query
        parameters.

        Args:
          query_param (dict): The `query_param` parameter is a dictionary that contains the parameters
        for filtering, sorting, limiting, skipping, and paginating the query.

        Returns:
          a list of queried data from the database.
        """
        query = self.db.query(self.model)

        queried_data: Query = Query(query=query, query_param=query_param)
        queries = queried_data.filter_by().sort().limit().skip().paginate()
        return queries.query.all()

    def update(self, update_data: dict, id: str):
        """
        The function updates a record in the database with the given update data and ID.

        Args:
          update_data (dict): The `update_data` parameter is a dictionary that contains the data to be
        updated. The keys of the dictionary represent the columns or fields to be updated, and the
        values represent the new values for those columns or fields.
          id (str): The `id` parameter is a string that represents the unique identifier of the object
        you want to update in the database.

        Returns:
          The `update` method is returning the result of the update operation. This could be the number
        of rows affected by the update or any other relevant information depending on the database
        library being used.
        """
        update = (
            self.db.query(self.model)
            .filter(self.model.id == id)  # type:ignore
            .update(update_data, synchronize_session="evaluate")
        )
        return update

    def delete(self, id: str):
        """
        The above function deletes a record from the database based on the provided ID.

        Args:
          id (str): The `id` parameter is a string that represents the unique identifier of the object
        that needs to be deleted from the database.
        """
        (
            self.db.query(self.model)
            .filter(self.model.id == id)  # type:ignore
            .delete(synchronize_session="evaluate")
        )

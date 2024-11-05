from typing import Any, TypeVar

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query

# Define type variables
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

Base = declarative_base()


class NewQueries:
    """Query helper class for handling filtering, sorting, and pagination"""
    def __init__(self, query: Query, request_query: dict[str, Any]):
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

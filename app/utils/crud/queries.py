from typing import Any, Dict

from sqlalchemy.orm import Query


class Queries:
    def __init__(self, model: Query, request_query: Dict[str, Any]):
        self.model = model
        self.request_query = request_query

    def filter(self):
        query_obj = self.request_query.copy()
        excluded_fields = ["page", "sort", "limit", "fields"]
        for field in excluded_fields:
            query_obj.pop(field, None)

        for key, value in query_obj.items():
            if isinstance(value, str):
                if key.endswith("__gte"):
                    self.model = self.model.filter(getattr(self.model.column_descriptions[0]['entity'], key[:-5]) >= value)
                elif key.endswith("__gt"):
                    self.model = self.model.filter(getattr(self.model.column_descriptions[0]['entity'], key[:-4]) > value)
                elif key.endswith("__lte"):
                    self.model = self.model.filter(getattr(self.model.column_descriptions[0]['entity'], key[:-5]) <= value)
                elif key.endswith("__lt"):
                    self.model = self.model.filter(getattr(self.model.column_descriptions[0]['entity'], key[:-3]) < value)
                else:
                    self.model = self.model.filter(getattr(self.model.column_descriptions[0]['entity'], key) == value)
            else:
                self.model = self.model.filter(getattr(self.model.column_descriptions[0]['entity'], key) == value)

        return self

    def sort(self):
        if "sort" in self.request_query:
            sort_by = self.request_query["sort"].split(",")
            for field in sort_by:
                if field.startswith("-"):
                    self.model = self.model.order_by(getattr(self.model.column_descriptions[0]['entity'], field[1:]).desc())
                else:
                    self.model = self.model.order_by(getattr(self.model.column_descriptions[0]['entity'], field).asc())
        else:
            self.model = self.model.order_by(getattr(self.model.column_descriptions[0]['entity'], "created_at").desc())

        return self

    def limit_fields(self):
        if "fields" in self.request_query:
            fields = self.request_query["fields"].split(",")
            self.model = self.model.with_entities(*[getattr(self.model.column_descriptions[0]['entity'], field) for field in fields])
        return self

    def paginate(self):
        page = int(self.request_query.get("page", 1))
        limit = int(self.request_query.get("limit", 100))
        offset = (page - 1) * limit

        self.model = self.model.offset(offset).limit(limit)

        return self

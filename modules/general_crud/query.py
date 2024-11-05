from cgi import print_environ
import zipimport
from sqlalchemy.orm import Session


class Query:
    def __init__(self, query, query_param: dict) -> None:

        self.query = query

        self.query_param = query_param
        nn = "limit" in self.query_param.keys()
        print(self.query_param.keys(), "query param don show", nn)

    def limit(
        self,
    ):
        if "limit" in self.query_param.keys():
            self.query = self.query.limit(self.query_param["limit"])
            print("i came insid limit")
            return self
        else:
            print("i came insid limit 2", self.query_param.keys())

            self.query = self.query.limit(100)
            return self

    def skip(
        self,
    ):
        if "skip" in self.query_param.keys():
            self.query = self.query.offset(self.query_param["skip"])
            return self
        else:
            self.query = self.query.offset(0)
            return self

    def paginate(self):
        """paginator

        Returns:
            self.query.limit:limits the query param to some certain data
        """
        if "page" in self.query_param.keys():
            if self.query_param["limit"]:
                limiter = self.query_param["limit"]
            else:
                limiter = 100
            skip = (self.query_param["page"] - 1) * limiter

            self.query = self.query.offset(offset=skip).limit(limit=limiter)
            return self
        else:
            self.query = self.query
            return self

    def filter_by(self):
        exclude = ["sort", "skip", "page", "limit"]
        new_query = self.query_param.copy()

        for data in exclude:
            if data in new_query:
                del new_query[data]

        if new_query is not None:

            self.query = self.query.filter_by(**new_query)
            return self

        else:
            self.query = self.query
            return self

    def sort(self):
        if "sort" in self.query_param.keys():
            self.query = self.query.order_by(self.query_param["sort"])
            return self
        else:
            self.query = self.query.order_by("id")
            return self

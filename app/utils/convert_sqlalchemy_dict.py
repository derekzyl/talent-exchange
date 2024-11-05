from collections.abc import Iterable
from datetime import datetime

from sqlalchemy.ext.declarative import DeclarativeMeta


def sqlalchemy_obj_to_dict(row):


    return row._asdict()


from typing import TypedDict


class WeeklyReport(TypedDict):
    name:str
    value:int    
# The `StatResponse` class is a TypedDict in Python.
class StatResponse(TypedDict):
    
    name:str
    count:str
    details:str
    weekly_reports:list[WeeklyReport]

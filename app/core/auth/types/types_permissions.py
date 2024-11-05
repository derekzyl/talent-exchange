from dataclasses import dataclass
from typing import TypedDict


@dataclass
class Permission:
    id: int
    name: str
    guard_name: str
    created_at: str  # Consider using a proper datetime type if available in your Python environment
    updated_at: str  # Consider using a proper datetime type if available in your Python environment




class PermissionT(TypedDict):
    id: int
    name: str
    guard_name: str
    created_at: str  # Consider using a proper datetime type if available in your Python environment
    updated_at: str  # Consider using a proper datetime type if available in your Python environment
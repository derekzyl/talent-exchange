

from enum import Enum
from typing import TypedDict

from fastapi import APIRouter, FastAPI

from app.core import auth
from app.core.auth.routes.auth_route import auth_router
from app.core.users.routes.routes_users import user_router
from app.versions.types_routes import RouterData

routesV1:list[RouterData]= [{
    'api_route':auth_router,'path':"auth",'tags':['auth'],
    
},{
    'api_route':user_router,'path':"users",'tags':['users']
}
                            ]


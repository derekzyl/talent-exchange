

from enum import Enum
from typing import TypedDict

from fastapi import APIRouter, FastAPI

from app.core import auth, skill_share
from app.core.auth.routes.auth_route import auth_router
from app.core.users.routes.routes_users import user_router
from app.core.skills.routes.route_skills import skill_router
from app.core.skills.routes.route_available_time import available_time_router
from app.core.reviews.routes.routes import review_router
from app.core.skill_share.routes.route_skill_share import skill_share_router
from app.core.skill_share.routes.ongoing_share_route import ongoing_share_router
from app.versions.types_routes import RouterData

routesV1:list[RouterData]= [{
    'api_route':auth_router,'path':"auth",'tags':['auth'],
    
},{
    'api_route':user_router,'path':"user",'tags':['users']
},{
    'api_route':skill_router,'path':"skill",'tags':['skills']
},{
    'api_route':available_time_router,'path':"available-times",'tags':['Available Times']}
,{
    'api_route':review_router,'path':"review",'tags':['reviews']
}, {
    'api_route':skill_share_router,'path':"skill-share",'tags':['skill-share']},{
    'api_route':ongoing_share_router,'path':"ongoing_router",'tags':['ongoing_skill-share']
    }
                       ]


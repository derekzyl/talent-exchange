from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.config.database.db import get_db, session_manager
from app.config.env import env
from app.core.auth.services.middleware_auth import AuthMiddleware
from app.versions.route_handler import handle_routing
from fastapi.middleware.cors import CORSMiddleware


def init_app(init_db=True):
    

     
    app:FastAPI = FastAPI(title="Skill Share App") 
    origins = [
    '*',
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5150",
]      
    app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
      # Add middleware before the lifespan context
    app.add_middleware(AuthMiddleware, db_session=session_manager) 

    

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            if init_db:
                session_manager.init(env["database_url"])
                async with session_manager.connect() as connection:
                    from app.core.users.models.model_user import UserModel
                    from app.core.notification.models.model_notification import NotificationModel
                    from app.core.auth.models.model_token import TokenModel
                    from app.core.skills.models.model_skills import SkillModel
                    from app.core.skills.models.model_available_time import SkillAvailableTimeModel
                    from app.core.reviews.model.model_reviews import ReviewModel
                    from app.core.skill_share.model.ongoing_share_model import OngoingSkillShareModel
                    from app.core.skill_share.model.skill_share_model import SkillShareRequestModel
                    from app.core.skill_share.model.skill_share_token import TokenSkillModel, TokenSkillTransactionModel
                
                    await session_manager.create_all(connection)
                    # await session_manager.drop_all(connection)
            yield
        finally:
            if session_manager._engine is not None:
                await session_manager.close()  
       
    app.router.lifespan_context=lifespan
    handle_routing(app=app)
    return app

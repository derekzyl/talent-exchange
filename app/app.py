from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.database.db import session_manager
from app.config.env import env
from app.versions.route_handler import handle_routing


def init_app(init_db=True):
    

     



    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            if init_db:
                session_manager.init(env["database_url"])
                async with session_manager.connect() as connection:
                    # await session_manager.create_all(connection)
                     await session_manager.drop_all(connection)
            yield
        finally:
            if session_manager._engine is not None:
                await session_manager.close()  
       
    app:FastAPI = FastAPI(lifespan=lifespan)       

    handle_routing(app=app)
    return app


# middleware/auth.py
import re
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from sqlalchemy.future import select as sa_select
from app.config.config import TokenType
from app.config.database.db import DatabaseSessionManager
from app.core.auth.models.model_token import TokenModel
from app.core.auth.services.service_token import TokenService
from app.core.users.models.model_user import UserModel
from app.core.users.services.service_user import UserService
from app.utils.convert_sqlalchemy_dict import sqlalchemy_obj_to_dict
from app.utils.crud.service_crud import AsyncSession, CrudService
from app.utils.crud.types_crud import ResponseMessage, response_message
from app.utils.logger import log

security = HTTPBearer()

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, db_session: DatabaseSessionManager):
        super().__init__(app)
        self.db = db_session
        # self.crud_service = CrudService(db=db_session, model=TokenModel) # type: ignore
        self.token_service = TokenService

    async def get_current_user(self, token: str) -> Optional[ResponseMessage]:
        # print("token", token)
        try:
            
            token_result: str = await self.token_service.verify_jwt_token(token=token )
       
            
            if not token_result:
                return ResponseMessage(
                    data=None, 
                    doc_length=0, 
                    error="Invalid or expired token", 
                    message="Unauthorized", 
                    success_status=False
                )
            
            user_service = UserServices(self.db)
        
            user = await user_service.get_one({"id":token_result}) 
            if not user or not user.get('data'):
                return ResponseMessage(
                    data=None, 
                    doc_length=0, 
                    error="User not found", 
                    message="Unauthorized", 
                    success_status=False
                )
                
            return user
        except Exception as e:
            print("error", e)
   
            log.logs.error(f"Error getting user: {e}")
            return None

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if self.should_skip_auth(request.url.path):
            
            return await call_next(request)

        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                raise HTTPException(
                    status_code=401,
                    detail=response_message(
                        error="Missing authorization header",
                        success_status=False,
                        message="Unauthorized"
                    )
                )

            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=401,
                    detail=response_message(
                        error="Invalid authentication scheme",
                        success_status=False,
                        message="Unauthorized"
                    )
                )

            current_user_response = await self.get_current_user(token)
            if not current_user_response or "data" not in current_user_response:
                raise HTTPException(
                    status_code=401,
                    detail=response_message(
                        error="Invalid or expired token",
                        success_status=False,
                        message="Unauthorized"
                    )
                )
            user = dict(current_user_response["data"])
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail=response_message(
                        error="Invalid or expired token ",
                        success_status=False,
                        message="Unauthorized"
                    )
                )

            # Add user to request state
            request.state.user = user
            
            response = await call_next(request)
            return response

        except HTTPException as exc:
            raise exc
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=response_message(
                    error=str(e),
                    success_status=False,
                    message="response error"
                )
            )

    def should_skip_auth(self, path: str) -> bool:
        """Define paths that should skip authentication"""
        public_paths = {
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/auth/login",
      
            "/api/v1/auth/signup",
            "/auth/register",
            
            
            
        }
        return any(path.startswith(public_path) for public_path in public_paths)


class UserServices:
    def __init__(self, db: DatabaseSessionManager):
        self.db = db
        self.model = UserModel

    async def get_one(self, data: dict[str, Any], select: Optional[list[str]] = None) -> ResponseMessage:
        async with self.db.session() as session:  # Obtain an AsyncSession
            try:
                query = sa_select(self.model).filter_by(**data)

                if select:
                    include_fields = [field for field in select if not field.startswith('-')]
                    exclude_fields = [field[1:] for field in select if field.startswith('-')]

                    if include_fields:
                        fields_to_select = [getattr(self.model, field) for field in include_fields]
                        query = sa_select(*fields_to_select).filter_by(**data)
                    else:
                        all_fields = set(self.model.__table__.columns.keys())
                        fields_to_select = [getattr(self.model, field) for field in all_fields if field not in exclude_fields]
                        query = sa_select(*fields_to_select).filter_by(**data)

                # Execute the query with AsyncSession
                result = await session.execute(query)
                db_item_selected = result.scalar()

                # Convert to dict for JSON serialization
                result_dict = sqlalchemy_obj_to_dict(db_item_selected)
                if isinstance(result_dict, dict) and "password" in result_dict:
                    del result_dict["password"]
                
                return response_message(
                    data=result_dict, 
                    doc_length=1, 
                    error=None, 
                    message="Data fetched successfully", 
                    success_status=True
                )
            except Exception as e:
                log.logs.error(f"Error executing query: {e}")
                return response_message(
                    data=None, 
                    doc_length=0, 
                    error=str(e), 
                    message="Error fetching data", 
                    success_status=False
                )
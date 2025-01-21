# middleware/auth.py
import re
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.config.config import TokenType
from app.core.auth.models.model_token import TokenModel
from app.core.auth.services.service_auth import TokenService
from app.core.users.services.service_user import UserService
from app.utils.crud.service_crud import AsyncSession, CrudService
from app.utils.crud.types_crud import ResponseMessage, response_message

security = HTTPBearer()

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, db_session: AsyncSession):
        super().__init__(app)
        self.db = db_session
        # self.crud_service = CrudService(db=db_session, model=TokenModel) # type: ignore
        self.token_service = TokenService

    async def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        # print("token", token)
        try:
            token_result: ResponseMessage = await self.token_service.verify_token(token=token, db=self.db, type=TokenType.ACCESS_TOKEN)
            print("token_result", token_result)

            if not token_result or not token_result.get('data'):
                return None
            
            user_service = UserService(self.db)
            user = await user_service.get_user_by_id(token_result['data']["user_id"]) # type: ignore
            if not user or not user.get('data'):
                return None
                
            return user['data'] # type: ignore
        except Exception:
            return None

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        print( "should_skip_auth", request.url.path)
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

            user = await self.get_current_user(token)
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail=response_message(
                        error="Invalid or expired token",
                        success_status=False,
                        message="Unauthorized"
                    )
                )

            # Add user to request state
            request.state.user = user
            
            response = await call_next(request)
            return response

        except HTTPException as exc:
            print("HTTPException", exc)
            raise exc
        except Exception as e:
            print("Exception", e)
            raise HTTPException(
                status_code=500,
                detail=response_message(
                    error=str(e),
                    success_status=False,
                    message="Internal server error"
                )
            )

    def should_skip_auth(self, path: str) -> bool:
        """Define paths that should skip authentication"""
        public_paths = {
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/auth/login",
            "/api/v1/auth/get-all-token",
            "/auth/register",
            
            
        }
        return any(path.startswith(public_path) for public_path in public_paths)

# # dependencies/auth.py
# from fastapi import Depends, Request, HTTPException
# from typing import Dict, Any

# async def get_current_user(request: Request) -> Dict[str, Any]:
#     user = getattr(request.state, "user", None)
#     if user is None:
#         raise HTTPException(
#             status_code=401,
#             detail=response_message(
#                 error="User not authenticated",
#                 success_status=False,
#                 message="Unauthorized"
#             )
#         )
#     return user

# # main.py
# from fastapi import FastAPI
# from app.middleware.auth import AuthMiddleware
# from app.config.database import get_db

# app = FastAPI()

# # Add middleware
# @app.on_event("startup")
# async def startup_event():
#     db = await get_db()
#     app.add_middleware(AuthMiddleware, db_session=db)

# # Example protected route
# @app.get("/protected")
# async def protected_route(current_user: Dict[str, Any] = Depends(get_current_user)):
#     return {
#         "message": "This is a protected route",
#         "user": current_user
#     }

# # Example public route
# @app.get("/public")
# async def public_route():
#     return {"message": "This is a public route"}
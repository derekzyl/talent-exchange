# handle middle ware for business users using their api key and api secret

from fastapi.exceptions import HTTPException


# def jwt normal user
# def jwt business user
# def api key auth



class MiddleWareService:
    def __init__(self, db:AsyncSession) -> None:
        self.crud_service = CrudService(db=db, model=TokenModel) # type: ignore
        self.user_service = UserService(db=db)
        self.business_service = BusinessService(db=db)
        self.db = db
    async def jwt_normal_user(self, request:Request, call_next):
        try:
            token = request.headers['Authorization']
            if token is None:
                raise HTTPException(status_code=400, detail=response_message(error="token not found", success_status=False, message="token not found"))
            token = token.split(" ")[1]
            token = await self.crud_service.get_one({"token":token})
            if token is None:
                raise HTTPException(status_code=400, detail=response_message(error="token not found", success_status=False, message="token not found"))
            user = await self.user_service.get_user_by_id(token['data']["user_id"])
            if user is None:
                raise HTTPException(status_code=400, detail=response_message(error="user not found", success_status=False, message="user not found"))
            request.state.user = user['data']
            response = await call_next(request)
            return response
        except Exception as e:
            raise HTTPException(status_code=400, detail=response_message(error=e, success_status=False, message="user not found"))
    async def jwt_business_user(self, request:Request, call_next):
        try:
            token = request.headers['Authorization']
            if token is None:
                raise HTTPException(status_code=400, detail=response_message(error="token not found", success_status=False, message="token not found"))
            token = token.split(" ")[1]
            token = await self.crud_service.get_one({"token":token})
            if token is None:
                raise HTTPException(status_code=400, detail=response_message(error="token not found", success_status=False, message="token not found"))
            user = await self.business_service.get_business_user_by_id(token['data']["user_id"])
            if user is None:
                raise HTTPException(status_code=400, detail=response_message(error="user not found", success_status=False, message="user not found"))
            request.state.user = user['data']
            response = await call_next(request)
            return response
        except Exception as e:
            raise HTTPException(status_code=400, detail=response_message(error=e, success
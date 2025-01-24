from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.users.models.model_user import UserModel
from app.core.users.types.type_user import CreateUserT, UpdateUserT
from app.utils.crud.service_crud import CrudService
from app.utils.crud.types_crud import response_message

# create a user
# delete a user
# update a user   
# get user by id 
# get user by email  
# get user by type


class UserService:
    def __init__(self, db:AsyncSession) -> None:
        self.crud_service = CrudService(db=db, model=UserModel) # type: ignore
        

    async  def create_user(self,data:CreateUserT ):
        try:
            d= dict(data)
            user =await self.crud_service.create(data=d, select=['-password'])
            return user
            
            
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=response_message(error=e, success_status=False, message="User not created"))    


    async def get_user_by_id(self, user_id: str):
        try:
            user = await self.crud_service.get_one({"id":user_id})
            return user
        except Exception as e:
            raise HTTPException(status_code=400, detail=response_message(error=e, success_status=False, message="User not found"))

    async def get_users(self, query:dict, filter:dict ):    # type: ignore
        try:
            users = await self.crud_service.get_many(query=query, filter=filter)
            
            return users
        except Exception as e:
            raise HTTPException(status_code=400, detail=response_message(error=e, success_status=False, message="User not found"))
    async def delete_user(self, user_id: str):
        try:
            await self.crud_service.delete({"id":user_id})
        except Exception as e:
            raise HTTPException(status_code=400, detail=response_message(error=e, success_status=False, message="User not deleted"))   
    async def get_user(self, data:dict):
        try:
            user = await self.crud_service.get_one(data=data,)
            return user
        except Exception as e:
         raise HTTPException(status_code=400, detail=response_message(error=e, success_status=False, message="User not found"))
    async def get_users_by_country(self, country: str, filter: dict|None= None):
        try:
            query = {"country": country}
            if filter is None:
                filter = {}
            users = await self.crud_service.get_many(query=query, filter=filter)
            return users
        except Exception as e:
            raise HTTPException(status_code=400, detail=response_message(error=e, success_status=False, message="Users not found"))

 
    async def update_user(self, filter:dict, data:UpdateUserT ):
        d=dict(data)
        try:
         dta=   await self.crud_service.update(filter=filter, data=d)
         return dta
         
        except Exception as e:
            raise HTTPException(status_code=400, detail=response_message(error=e, success_status=False, message="User not updated"))     

    @staticmethod
    def get_logged_in_user(request:Request):
  
        user = getattr(request.state, "user", None)
        
        if not user:
            raise HTTPException(status_code=401, detail=response_message(error="User not authorized", success_status=False, message="User not authorized"))

        else:
            return user
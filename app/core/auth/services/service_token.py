import math
import random
from datetime import datetime, timedelta
from tabnanny import check
from typing import TypedDict

from fastapi import HTTPException
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import env
from app.config.config import TokenType
from app.config.database import db
from app.core.auth.models.model_token import TokenModel
from app.core.users.types.type_user import UserT
from app.utils.crud.service_crud import CrudService
from app.utils.crud.types_crud import response_message
from app.utils.logger import log
from app.utils.my_jwt import MyJwt

jwt = MyJwt()


class saveToken(TypedDict):
    token:str
    expires:int
    type:str
    user_id:str
    blacklisted:bool
class TokenService:
    def __init__(self, db:AsyncSession) -> None:
        self.db = db
        self.crud_service = CrudService(db=db, model=TokenModel) # type: ignore

        
    async def get_all_tokens(self):
       data = await self.crud_service.get_many({})
       return data
        
    
    @staticmethod
    def generate_token (user_id:str, token_type:str ,expires_in:int) -> str:
        return jwt.create_token(subject=user_id,token_type=token_type, expires_in=expires_in)

    @staticmethod
    def generate_otp_token(otp_length:int=6) -> int:
        otp:int = math.floor(random.random() * (10 ** otp_length))
        return otp

    @staticmethod
    async def save_token(data:saveToken, db:AsyncSession):

        get_existing_token =await CrudService(db=db, model=TokenModel).get_one(data={"user_id":data['user_id'], "type":data['type']}) # type: ignore

        # log.logs.info(f"get_existing_token {get_existing_token}")
        if "data" in get_existing_token and get_existing_token["data"] is not None:  # type: ignore
            stmt =(update(TokenModel).values(blacklisted=True).where(TokenModel.id == get_existing_token['data'][0].id)) # type: ignore
            await db.execute(stmt)
        data['expires'] = datetime.now() + timedelta(minutes=data['expires']) # type: ignore
        token_data = TokenModel(**data)
        db.add(token_data)
        await db.commit()
        await db.refresh(token_data)
        return token_data
    @staticmethod
    async def verify_token(token:str, type:TokenType, db:AsyncSession):
        token_data = jwt.verify_token(token=token)

  
        
        if isinstance(token_data['sub'], str)==False:
            raise HTTPException(
                status_code=400,
                                detail=response_message(error="Invalid token", success_status=False, message="Invalid token")
            )
        try:
            token_data = await db.get_one(TokenModel, {
                "user_id": token_data['sub'],
                
                "type": type.value,
                "blacklisted": False
                })

            stmt =(update(TokenModel).values(blacklisted=True).where(TokenModel.id == token_data.id))
            await db.execute(stmt)
       
            if token_data is None:
                raise HTTPException(
                    status_code=400,
                                    detail=response_message(error="Invalid token", success_status=False, message="Invalid token")
                )
            return token_data    
        except Exception as e:
            raise HTTPException(
                status_code=400,
                                detail=response_message(error=e, success_status=False, message="Invalid token")
            )    




    @staticmethod
    async def verify_jwt_token(token:str):
        token_data = jwt.verify_token(token=token)

        
        if isinstance(token_data['sub'], str)==False:
            raise HTTPException(
                status_code=400,
                                detail=response_message(error="Invalid token", success_status=False, message="Invalid token")
            )
        try:
            # check if token has expired

            token_time = token_data['exp']
           
            if datetime.fromtimestamp(token_time) < datetime.now():
                raise HTTPException(
                    status_code=400,
                                    detail=response_message(error="Invalid token", success_status=False, message="Invalid token")
                )


            return token_data["sub"]   
                
            
             
        except Exception as e:
            raise HTTPException(
                status_code=400,
                                detail=response_message(error=e, success_status=False, message="Invalid token")
            )    
   


    @staticmethod
    async def verify_otp_token(token:str, user_id:str, type:TokenType, db:AsyncSession):
        try:
            token_data = await db.get_one(TokenModel, {
                "user_id": user_id,
                "type": type.value,
                "blacklisted": False,
                "token":token
                })
            # update
            stmt =(update(TokenModel).values(blacklisted=True).where(TokenModel.id == token_data.id))
            await db.execute(stmt)
            if token_data is None:
                raise HTTPException(
                    status_code=400,
                                    detail=response_message(error="Invalid token", success_status=False, message="Invalid token")
                )

            if datetime.strptime(token_data.expires,"%Y-%m-%d %H:%M:%S") < datetime.now():
                raise HTTPException(
                    status_code=400,
                                    detail=response_message(error="Invalid token", success_status=False, message="Invalid token")
                )   
            return token_data
        
        except Exception as e:
            raise HTTPException(
                status_code=400,
                                detail=response_message(error=e, success_status=False, message="Invalid token")
            )

    @staticmethod
    async def generate_auth_token(user_id:str,db:AsyncSession):
        access_expiry_time = env.env['jwt']['jwt_access_expiry_time']
        refresh_expiry_time = env.env['jwt']['jwt_refresh_expiry_time']

        access_token = MyJwt().create_token(subject=user_id, token_type=TokenType.ACCESS_TOKEN.value, expires_in=access_expiry_time)
        refresh_token = MyJwt().create_token(subject=user_id, token_type=TokenType.REFRESH_TOKEN.value, expires_in=refresh_expiry_time)

        await TokenService.save_token(data={
            "token":refresh_token,
            "expires":access_expiry_time,
            "type":TokenType.REFRESH_TOKEN.value,
            "user_id":user_id,
            "blacklisted":False
        }, db=db)

        return {
        "access":{"token":access_token, "expires":datetime.now()+  timedelta(minutes=access_expiry_time)},
        "refresh":{"token":refresh_token, "expires":datetime.now()+ timedelta(minutes=refresh_expiry_time)}
        }

    @staticmethod
    async def refresh_auth_token(refresh_token:str, db:AsyncSession):
        get_user =await TokenService.verify_token(token=refresh_token, type=TokenType.REFRESH_TOKEN, db=db )
        generate_user_token = await TokenService.generate_auth_token(user_id=get_user.id, db=db)
        return generate_user_token


    def generate_reset_password_token():
        pass

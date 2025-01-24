

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import class_mapper

from app.config import env
from app.config.config import TokenType

from app.core.auth.services.service_token import TokenService
from app.core.auth.types.types_auth import ChangePassWordT, LoginT
from app.core.notification.service.mailer import Mailer
from app.core.users.models.model_user import UserModel
from app.core.users.services.service_user import UserService
from app.core.users.types.type_user import CreateUserT, UserT
from app.utils import password_hash
from app.utils.convert_sqlalchemy_dict import sqlalchemy_obj_to_dict
from app.utils.crud.service_crud import CrudService
from app.utils.crud.types_crud import response_message
from app.utils.logger import log
from app.utils.regex import email_regex, password_regex


class AuthService(UserService):
    def __init__(self, db:AsyncSession) -> None:
        super().__init__(db)
        self.db = db

    async def create(self, data:CreateUserT):
        try:
            password = password_hash.PassHash().hash_me(data['password']) 
            if not password_regex.match(data["password"]):
                raise HTTPException(status_code=400, detail=response_message(error="invalid password", success_status=False, message="password must be 8 character long with uppercase lowercase number and special character") )   
            if not email_regex.match(data["email"]):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_message(error="email is not valid", success_status=False, message="email not valid kindly check your email and retry"))
            #check if the user does exist
            
            user = select(UserModel).filter(UserModel.email == data["email"])
        
            result =(await  self.db.scalars(user)).one_or_none()
            if result:# type: ignore
                
                raise HTTPException(status_code=400, detail=response_message(error="user already exist", success_status=False, message="user already exist kindly login to continue"))

            del data["password"] # type: ignore
            user = await self.create_user(data={"password": password, **data})
            if user["data"] is None: # type: ignore
                raise HTTPException(status_code=400, detail=response_message(error="user not created", success_status=False, message="User not created")) 
            
            db_user = user["data"] # type: ignore
            
            token = await TokenService.generate_auth_token(db_user.id, db=self.db )
            
            d = sqlalchemy_obj_to_dict(db_user)
            if isinstance(d, dict):
                d.pop('password', None)
            else:
                del d.password    # type: ignore
            
            
            return {'user':d,
                    "token":token}
        except Exception as e:
            log.logs.error(f"error creating user {e}")
            return e
        finally:
            await self.db.close()
        
        
    async def login(self, data:LoginT):

        #  lets find the user 

        if email_regex.match(data["email"]): 
            user = await self.get_user({"email":data['email']})
        else:
            user = await self.get_user({"username":data['email']})
        if user and user['data'] is None: # type: ignore
            raise HTTPException(status_code=400, detail=response_message(error="login error", success_status=False, message="incorrect username or password"))

        

        if not password_hash.PassHash().verify_me(password=data['password'], hashed_password=user['data'][0].password): # type: ignore
            raise HTTPException(status_code=400, detail=response_message(error="login error", success_status=False, message="incorrect username or password"))

        db_user =user['data'][0] # type: ignore
        

 
        
      
    
        
        token = await TokenService.generate_auth_token(db_user.id, db=self.db )
        if isinstance(db_user, dict):
            db_user.pop('password', None)
        else:
            del db_user.password  
        return {'user':db_user,
                "token":token}
    async def reset_password(self, data:dict):

        get_user =  await self.get_user(data=data['email'])

        if get_user["data"] is None:  # type: ignore
           
            raise HTTPException(status_code=400, detail=response_message(error="user not found", success_status=False, message="user not found"))
        
        get_token =await TokenService.verify_otp_token(db=self.db, user_id=get_user['data']["id"], token= data['token'], type=TokenType.RESET_PASSWORD,) # type: ignore

        if get_token is not None:
            stmt= update(UserModel).where(UserModel.id == get_user['data']["id"]).values(password=password_hash.PassHash().hash_me(data['password'])) # type: ignore
            await self.db.execute(stmt)
            
            return response_message(success_status=True, message="password changed", data="password changed successfully")

        
    async def send_email_verification(self, data:dict, background_task:BackgroundTasks):

        user = await self.get_user_by_id(data['user_id'])

        if user["data"] is None: # type: ignore
            raise HTTPException(status_code=400, detail=response_message(error="user not found", success_status=False, message="user not found"))

        token = generate_otp_token(user_id=user['data']["id"], expires_in=30, token_type=TokenType.VERIFY_EMAIL) # type: ignore

        if env.env["mail"]["use_mail_service"] is True:
            mail =Mailer(background=True, background_tasks=background_task, body={"website_name":"medic", "expiry_time": 30, 'otp':token}, html_template='verification/verify_email', receiver_email=user["data"]['email'], subject='verify email') # type: ignore

            await mail.sendmail()
        return response_message(success_status=True, message="email sent successfully", data="verification email sent")
  
    async def change_password(self, data:dict):
        user = await self.get_user_by_id(data["user_id"])
        
        if user["data"] is None: # type: ignore
            raise HTTPException(status_code=400, detail=response_message(error="user not found", success_status=False, message="user not found"))
    async def logout(self, data:dict):        
        
       return {'token':""}
    async def verify_email(self, data:dict):
        get_token =  await TokenService.verify_otp_token(db=self.db, user_id=data['user_id'], token= data['token'], type=TokenType.VERIFY_EMAIL, )
        if get_token is not None:
            stmt= update(UserModel).where(UserModel.id == data['user_id']).values(is_verified=True)
            await self.db.execute(stmt)
            return response_message(success_status=True, message="email verified", data="email verified successfully")

        
    async def forgot_password(self, data:dict, background_task:BackgroundTasks):
        user = await self.get_user({"email":data['email']})
        if 'data' in user and user['data'] is None: # type: ignore
            raise HTTPException(status_code=400, detail=response_message(error="email sent successfully", success_status=False, message="if you have an account, an email has been sent to you to proceed with reset password"))

        token = TokenService.generate_token(user_id=user['data']["id"], expires_in=30,  token_type=TokenType.RESET_PASSWORD) # type: ignore

        
        

        if env.env["mail"]["use_mail_service"] is True:
            mail =Mailer(background=True,background_tasks=background_task, body={"website_name":"medic", "expiry_time": 30, 'otp':token}, html_template='verification/rest_password', receiver_email=user["data"]['email'], subject='change password')  # type: ignore

            await mail.sendmail()
        return response_message(success_status=True, message="email sent successfully", data="if you have an account, an email has been sent to you to proceed with reset password")    
        
       




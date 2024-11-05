from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import notification
from app.core.notification.models.model_notification import NotificationModel
from app.utils.crud.service_crud import CrudService

#user services

#staff services

#admin  services
class NotificationService(CrudService):
    def __init__ (self, db:AsyncSession):
        super().__init__(db=db, model=NotificationModel) # type: ignore
        self.db = db


    async def  send_notification(self, data: dict):
        


        notification = await self.create(data=data)
        return notification

         


        

    async def get_notification(self, data: dict):
        notification = await self.get_one(data=data)
        return notification

       

    async def update_notification(self, data: dict, filter:dict):

        notification = await self.update(data=data, filter=filter)
        return notification


    async def delete_notification(self, data: dict):

        await self.delete(data)
    async def get_notifications(self, filter: dict, query:dict):

        notification = await self.get_many(query= query, filter=filter) 
        return notification
    async def get_notification_by_id(self, id:str):

        notification = await self.get_one(data={"id":id})
        return notification
    async def get_notification_by_user_id(self, query:dict, user_id:str):

        notification = await self.get_many(query=query, filter={"user_id":user_id})
        return notification
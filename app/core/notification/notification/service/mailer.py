from typing import Any

from fastapi import BackgroundTasks, HTTPException, status
from fastapi_mail import ConnectionConfig, FastMail, MessageType
from fastapi_mail.schemas import MessageSchema
from pydantic import BaseModel, EmailStr

from app.config import env
from app.utils.template import renderTemplate


class Mailer:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        receiver_email: list[EmailStr],
        html_template: str,
        subject: str,
        body: dict[str, Any],
        background: bool = False,
        
    ):
        self.sender_email: EmailStr = env.env["mail"]["mail_sender"]
        self.background = background
        self.background_tasks = background_tasks
        self.html_template = html_template

        self.config = ConnectionConfig(
            MAIL_SERVER=env.env['mail']['mail_server'],
            MAIL_PORT=env.env["mail"]["mail_port"],
            MAIL_USERNAME=env.env["mail"]["mail_username"],
            MAIL_PASSWORD=env.env["mail"]["mail_password"],
            MAIL_FROM=env.env["mail"]["mail_sender"],
            MAIL_FROM_NAME="medic",
            MAIL_SSL_TLS=False,
            VALIDATE_CERTS=True,
            MAIL_STARTTLS=True,
            USE_CREDENTIALS=True,
        )

        self.message = MessageSchema(
            subject=subject,
            recipients=receiver_email,
            template_body=renderTemplate(directory=self.html_template, data=body),
            subtype=MessageType.html,
        )

    async def sendmail(self):
        fm = FastMail(self.config)
        if self.background:
            self.background_tasks.add_task(fm.send_message, self.message)
            return {"message": "email sent successfully"}
        else:
            send = await fm.send_message(self.message)

            if send:
                return {"message": "email sent successfully"}
            else:
                return HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=send
                )

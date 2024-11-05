from webbrowser import get

from fastapi import (
    APIRouter,
    Body,
    Depends,
    BackgroundTasks,
    Request,
    status,
    HTTPException,
)
from fastapi.responses import JSONResponse
from modules.auth.services.factory import UserFactory

from sqlalchemy.orm import Session
from modules.auth.services.protector import protector
from modules.auth.model.model import UserModel
from modules.auth.model import model
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from modules.auth.schema.schema import (
    PasswordChange,
    ResetPassword,
    UserInDbSchema,
    UserSignupSchema,
)
from server.db import get_db, engine
from utils.notifications.services.mailer import Mailer
from utils.my_jwt import MyJwt
from datetime import datetime
from typing import Annotated, Any
from jose.exceptions import JWTError
from modules.auth.model.model import UserModel
from utils.response_message import responseMessage

from utils.types_utils.response_types import ResponseT
from pathlib import Path

userRouter: APIRouter = APIRouter(prefix="/auth")
model.Base.metadata.create_all(bind=engine)  # type: ignore

# TODO: updating online presence with websocket


@userRouter.post("/signup")
async def signup(
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    mUser = await request.body()
    data = mUser.decode(encoding="utf-8")

    myUser = UserSignupSchema.parse_raw(data)

    userCreate: UserFactory = UserFactory(db=db, model=UserModel)  # type: ignore
    created_user = userCreate.createUser(user=myUser)
    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="something went wrong creating user",
        )
    url: str = (
        request.url.hostname if request.url.hostname is not None else "localhost:5000/"
    )
    get_token: str = created_user["token"]

    email_data = {
        "verification_link": url + "/verify-email/" + get_token,
        "website_name": request.url.hostname,
        "expiry_time": created_user["user"].token_expiry_time,
    }

    mailing = Mailer(
        html_template="verify_email.html",
        background_tasks=background_tasks,
        background=True,
        body=email_data,
        receiver_email=[created_user["user"].email],
        subject="Email verification ",
    )
    await mailing.sendmail()

    jw = MyJwt()
    token = jw.create_token(subject=created_user["user"].id, expires=300)  # type: ignore
    return JSONResponse(
        content=responseMessage(
            {
                "data": {"token": token},
                "message": "user successfully created",
                "success_status": True,
            }
        ),
        status_code=status.HTTP_201_CREATED,
        headers={"authorization": f"Bearer {token}"},
    )


@userRouter.post(path="/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    userLogin: UserFactory = UserFactory(db=db, model=UserModel)  # type: ignore
    logged = userLogin.login(username=form.username, password=form.password)
    if logged is not None:
        jw = MyJwt()
        token = jw.create_token(
            subject=logged.id,
            expires=300,
        )  # type: ignore
        return JSONResponse(
            content={
                "message": "login successfully",
                "token": token,
                "status": True,
            },
            status_code=status.HTTP_202_ACCEPTED,
        )


@userRouter.post(path="/change_password")
def changePassword(
    body: Annotated[PasswordChange, Body(embed=True)],
    user=Annotated[UserInDbSchema, Depends(protector)],
    db=Annotated[Session, Depends(dependency=get_db)],
):
    user_factory = UserFactory(db=db, model=UserModel)
    password_change = user_factory.changePassword(
        user=user, old_password=body.old_password, new_password=body.new_password
    )
    return JSONResponse(
        content=responseMessage(
            data={
                "data": {"message": "password changed successfully"},
                "message": "password changed successful",
                "success_status": True,
            }
        ),
        status_code=status.HTTP_202_ACCEPTED,
    )


@userRouter.post(path="reset-password")
def resetPassword(
    background_tasks: BackgroundTasks,
    body: Annotated[str, Body(embed=True)],
    db: Session = Depends(dependency=get_db),
):
    # get the user
    reset_password_factory = UserFactory(db=db, model=UserModel)

    get_the_reset = reset_password_factory.resetPassword(
        email=body, background_task=background_tasks
    )
    return JSONResponse(
        content=responseMessage(
            data={
                "data": {"message": get_the_reset},
                "message": "password reset process has been sent to your email address, kindly jump on to your email to verify",
                "success_status": True,
            }
        ),
        status_code=status.HTTP_202_ACCEPTED,
    )


@userRouter.post(path="/reset-password/{token}")
def resetPasswordToken(
    new_password: Annotated[str, Body(embed=True)],
    token: Annotated[str, Path(embed=True)],
    db: Session = Depends(dependency=get_db),
):
    password_reset_factory = UserFactory(db=db, model=UserModel)
    password_reset: str = password_reset_factory.resetPasswordWithToken(
        token=token, new_password=new_password
    )
    return JSONResponse(
        content=responseMessage(
            data={
                "data": {"message": password_reset},
                "message": "password reset successfully",
                "success_status": True,
            }
        ),
        status_code=status.HTTP_202_ACCEPTED,
    )


@userRouter.post(path="/logout")
def logout(
    user: Annotated[UserInDbSchema, Depends(dependency=protector)],
    db: Session = Depends(dependency=get_db),
):
    logout_factory = UserFactory(db=db, model=UserModel)
    logout = logout_factory.logout(user=user)
    return JSONResponse(
        content=responseMessage(
            data={
                "data": {"message": logout, "token": None},
                "message": "logout successfully",
                "success_status": True,
            }
        ),
        status_code=status.HTTP_202_accepted,
    )

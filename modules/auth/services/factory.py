import datetime
import re

from typing import Any, Generic, TypeVar

from pydantic import EmailStr
from modules.auth.schema.schema import (
    ResetPassword,
    TokenTypeE,
    UserInDbSchema,
    UserSignupSchema,
)
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends


from server.db import Base
from utils.crypto import EncryptAndCompareData
from utils.notifications.services.mailer import Mailer
from utils.password_hash import PassHash
from utils.regex import email_regex, password_regex
from fastapi import BackgroundTasks
from utils.response_message import responseMessage

# from utils.mailer import Mailer

# from utils.my_jwt import MyJwt
from utils.uuid_generator import id_uuid


modelType = TypeVar(name="modelType", bound=Base)
db = TypeVar(name="db", bound=Session)


class UserFactory(Generic[modelType, db]):
    """user factory to run crud operation for the user flow"""

    def __init__(self, db: Session, model: type[modelType]) -> None:
        self.db: Session = db

        self.model: type[modelType] = model

    def createUser(
        self,
        user: UserSignupSchema,
    ) -> dict[str, Any] | None:
        """create user

        Args:
            user (UserSignupSchema): takes a json data containing username password email and confirm password

        Raises:
            HTTPException: if email is invalid
            HTTPException: password is not containing alphanumeric and special character
            HTTPException: password length is less than 6
            HTTPException: if user exist in database
            HTTPException: if email is invalid
            HTTPException: is username is less than 3 character


        Returns:
            _type_: _description_
        """
        user_email = None

        if re.match(pattern=email_regex, string=user.email):
            user_email = (
                self.db.query(self.model).filter(self.model.email == user.email).first()  # type: ignore
            )  # type: ignore
        else:
            user_email = (
                self.db.query(self.model)
                .filter(self.model.username == user.username)  # type: ignore
                .first()
            )  # type: ignore

        if user_email:
            raise HTTPException(
                status_code=500,
                detail=responseMessage(
                    data={
                        "data": {"message": "user already exist"},
                        "message": "user already exist",
                        "success_status": False,
                    }
                ),
            )
        if not user_email:
            if user.password != user.confirm_password:
                raise HTTPException(
                    status_code=403,
                    detail=responseMessage(
                        data={
                            "data": {"message": "password doesn't match up"},
                            "message": "password doesn't match up",
                            "success_status": False,
                        }
                    ),
                )
            if len(user.password) < 6:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="password must contain more than one character",
                )
            if not re.fullmatch(email_regex, user.email):
                raise HTTPException(status_code=402, detail="email is invalid")

            if not re.fullmatch(pattern=password_regex, string=user.password):
                raise HTTPException(
                    status_code=402,
                    detail="password must contain uppercase, lowercase number and a special character",
                )
            if (
                not user.email
                and not user.username
                and not user.password
                and not user.confirm_password
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="field cannot be empty",
                )
            if len(user.username) < 3:
                raise HTTPException(
                    status_code=status.HTTP_411_LENGTH_REQUIRED,
                    detail="the username is too short",
                )
            password_hash = PassHash().hash_me(user.password)
            # now we proceed to email verification link to the user mail

            # 1) we generate a random string and then harsh it

            uuid_data = id_uuid()
            random_string = TokenTypeE.EMAIL + uuid_data

            # 2) encrypt the the token generated
            token = EncryptAndCompareData()
            token = token.sign(data=random_string)
            token_expiry_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5)

            user = self.model(
                email=user.email,
                username=user.username,
                password=password_hash,
                token=token,
                token_expiry_time=token_expiry_time,
            )

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            return {"user": user, "token": random_string}

    def login(self, username: str, password: str):
        """
        The `login` function checks if the provided username or email exists in the database, validates
        the password, and returns the user if the login is successful.

        :param username: The `username` parameter is a string that represents the username or email of
        the user trying to log in
        :type username: str
        :param password: The `password` parameter is a string that represents the password entered by
        the user during the login process
        :type password: str
        :return: The `login` method returns the `username_or_email` object if the username and password
        are correct.
        """

        username_or_email: UserInDbSchema | None = None

        if re.match(pattern=email_regex, string=username):
            username_or_email: UserInDbSchema | None = (
                self.db.query(self.model).filter(self.model.email == username).first()  # type: ignore
            )
        else:
            username_or_email = (
                self.db.query(self.model)
                .filter(self.model.username == username)  # type: ignore
                .first()
            )

        if not username_or_email:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="wrong username or password kindly check your username and password",
            )

        if not re.fullmatch(pattern=password_regex, string=password):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="incorrect username or password",
            )
        if len(password) < 6:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="incorrect username or password",
            )
        if username_or_email:
            pass_hash = PassHash()
            check_password = pass_hash.verify_me(
                password=password, hashed_password=username_or_email.password
            )
            if check_password:
                return username_or_email
            else:
                raise HTTPException(
                    status_code=status.HTTP_417_EXPECTATION_FAILED,
                    detail="incorrect username or password",
                )

    def verifyEmail(self, token: str) -> str:
        """
        The function verifies an email by checking the token against the encrypted token stored in the
        database and updates the user's "is_email_verified" field to True if the token is valid.

        :param token: The `token` parameter is a string that represents the verification token for the
        email
        :type token: str
        :return: a string "email verified successfully" if the email verification is successful.
        """

        # 1)  we start with getting the id of the email token
        # 2) encrypt the the token generated
        cryp = EncryptAndCompareData()
        tryp = cryp.sign(data=token)

        # 3) we find the existing user with the token
        user = self.db.query(self.model).filter(self.model.token == tryp).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="invalid verification link",
            )

        user.update({"is_email_verified": True}, synchronize_session=True)

        return "email verified successfully"

    async def resetPassword(
        self,
        email: str,
        background_task: BackgroundTasks,
        hostname: str | None = None,
    ):
        # 1) wé find if the email does exist
        user: modelType | None = (
            self.db.query(self.model).filter(self.model.email == email).first()
        )
        if not user:
            return "password verification process has been sent to your email address, kindly jump on to your email to verify"
        else:
            # we send email to the user
            url: str = hostname if hostname is not None else "localhost:5000/"
            # 1) we generate a random string and then harsh it

            uuid_data = id_uuid()
            random_string = TokenTypeE.Password + uuid_data

            # 2) encrypt the the token generated
            token = EncryptAndCompareData()
            token = token.sign(data=random_string)
            token_expiry_time = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=30
            )
            email_data = {
                "verification_link": url + "/reset-password/" + token,
                "website_name": hostname,
                "expiry_time": user["token_expiry_time"],
            }

            mailing = Mailer(
                html_template="reset_password.html",
                background_tasks=background_task,
                background=True,
                body=email_data,
                receiver_email=[EmailStr(user["email"])],
                subject="Password Reset ",
            )
            await mailing.sendmail()
            user.update(
                {
                    "token": random_string,
                    "token_expiry_time": token_expiry_time,
                }
            )
            return "password verification process has been sent to your email address, kindly jump on to your email to verify"

    def changePassword(
        self, user: UserInDbSchema, old_password: str, new_password: str
    ):
        # 1) compare passwords
        password = PassHash().verify_me(
            hashed_password=user.password, password=old_password
        )
        if not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="old password is not valid",
            )
        # 2) check if new_password passes password regex

        pas = re.fullmatch(pattern=password_regex, string=new_password)
        if not pas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password is not valid include uppercase ,lowercase, number and symbol and must be more than 8 character",
            )
        # 3) encrypt the new password

        hashed_password = PassHash().hash_me(password=new_password)

        done = (
            self.db.query(self.model)
            .filter(self.model.id == user.id)
            .update(values={"password": hashed_password})
        )
        if not done:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="server couldn't update password",
            )

        return "password updated successfully"

    def logout(self, user: UserInDbSchema):
        """
        The `logout` function removes the token from the database for a given user and returns a success
        message.

        :param user: The `user` parameter is an instance of the `UserInDbSchema` class. It represents
        the user for whom the logout operation is being performed
        :type user: UserInDbSchema
        :return: the string "logout successfully" if the logout process is completed successfully.
        """
        # 1) we remove the token from the database
        done = (
            self.db.query(self.model)
            .filter(self.model.id == user.id)
            .update(values={"token": None})
        )
        # 2) clear the jwt token

        if not done:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="server couldn't update password",
            )

        return "logout successfully"

    def resetPasswordWithToken(self, token: str, new_password: str):
        """
        The `resetPasswordWithToken` function checks the token against the encrypted token stored in the
        database and updates the user'XX"is_email_verified" field to True if the token is valid.

        :param token: The `token` parameter is a string that represents the verification token for the
        email
        :type token: str
        :return: a string "email verified successfully" if the email verification is successful.
        """

        # 1)  we start with getting the id of the email token
        # 2) encrypt the the token generated
        cryp = EncryptAndCompareData()
        tryp = cryp.sign(data=token)

        # 3) we find the existing user with the token
        user = self.db.query(self.model).filter(self.model.token == tryp).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="invalid verification link",
            )

        # 4) check if new_password passes password regex
        pas = re.fullmatch(pattern=password_regex, string=new_password)
        if not pas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password is not valid include uppercase ,lowercase, number and symbol and must be more than 8 character",
            )
        # 5 encrypt new password
        encrypt_password = PassHash().hash_me(password=new_password)

        # 6) update user in data base

        update_user = (
            self.db.query(self.model)
            .filter(self.model.id == user.id)
            .update(values={"password": encrypt_password, "is_email_verified": True})
        )
        return "password updated successfully"

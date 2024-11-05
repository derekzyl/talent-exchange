from datetime import datetime, timedelta
from enum import Enum
from typing import Any, TypedDict

from jose import jwt

from app.config import env

jwt_secret: str = env.env['jwt']["jwt_secret"]



class MyJwt:
    def __init__(
        self,
    ):
        self.JWT_SECRET: str = jwt_secret
        self.IAT = datetime.now()

    def create_token(self, subject: str,  token_type: str|Enum , expires_in: int):
        payload = {}
        expire = timedelta(minutes= expires_in)
        payload["exp"] = datetime.now() + expire
        payload["iat"] = datetime.now()
        payload["type"] = token_type
        payload["sub"] = subject
        payload["alg"] = "RS256"

        return jwt.encode(claims=payload, key=self.JWT_SECRET)

    def verify_token(self, token: str)-> dict[str, Any]:
        return jwt.decode(token=token, key=self.JWT_SECRET)



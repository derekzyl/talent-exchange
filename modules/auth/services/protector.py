from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from modules.auth.model.model import UserModel
from modules.auth.schema.schema import UserInDbSchema
from server.db import get_db
from utils.my_jwt import MyJwt

oauth = OAuth2PasswordBearer(tokenUrl="/token")


def myGuard(token: OAuth2PasswordBearer = Depends(oauth)) -> OAuth2PasswordBearer:
    """my guard takes token, header token as an argument and returns the user

    Args:
        token (OAuth2PasswordBearer, optional): _description_. Defaults to Depends(oauth).

    Returns:
        _type_: USER


    """
    print("finally gotten to my guard")

    return token


def verifiedUser(user: UserInDbSchema = Depends(myGuard)):
    """it checks if the user is verified

    Args:
        user (UserInDbSchema, optional): _description_. Defaults to Depends(myGuard).

    Raises:
        HTTPException: error if the user isnt verified

    Returns:
        _type_: verified user
    """

    if not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="user is not verified",
        )
    else:
        return user


def protector(token: str = Depends(myGuard), db: Session = Depends(get_db)):
    try:
        jw = MyJwt()
        h = jw.verify_token(token=token)
        print(f"hhhhh {h}")
        my_exp = datetime.fromtimestamp(int(h["exp"]))
        if my_exp < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="expired login token",
            )
        user_i = h["sub"]
        print(user_i)
        user = db.query(UserModel).filter(UserModel.id == user_i).first()  # type: ignore

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid jwt token"
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Exception())


def userAndEmailVerified(user: UserInDbSchema = Depends(protector)):
    if not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="the user is not verified to carry ou this action",
        )
    if user.is_email_verified:
        return user

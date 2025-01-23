from typing import TypedDict


class LoginT(TypedDict):
    email:str
    password:str


class ChangePassWordT(TypedDict):
    old_password:str
    new_password:str
    confirm_password:str
  
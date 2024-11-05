# def decorate(func):
#     def inner(ho: str):
#         na = ho.upper()
#         func(na)
#         print("hello world")

#     return inner()


# @decorate
# def me(ho: str):
#     print("hello" + ho)
# from hashlib import blake2b
# from hmac import compare_digest

# SECRET_KEY = b"pseudorandomly generated server secret key"
# AUTH_SIZE = 16


# def sign(cookie):
#     h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
#     h.update(cookie)
#     return h.hexdigest().encode("utf-8")


# def verify(cookie, sig):
#     good_sig = sign(cookie)
#     print(compare_digest(good_sig, sig))
#     return compare_digest(good_sig, sig)


# import _collections_abc


# class ListBasedSet(_collections_abc.Set):  # type: ignore
#     """Alternate set implementation favoring space over speed
#     and not requiring the set elements to be hashable."""

#     def __init__(self, iterable):
#         self.elements = lst = []
#         for value in iterable:
#             if value not in lst:
#                 lst.append(value)

#     def __iter__(self):
#         print(iter(self.elements))
#         return iter(self.elements)

#     def __contains__(self, value):
#         return value in self.elements

#     def __len__(self):
#         print(len(self.elements))
#         return len(self.elements)


# s1 = ListBasedSet("abcdef")
# s2 = ListBasedSet("defghi")
# overlap = s1 & s2

# from fastapi.encoders import jsonable_encoder

# d = {"hello": "world"}

# print(jsonable_encoder(d))
# game = {"adam": "name", "age": 50}
# good = {**game, "nude": True}
# print(good)

from datetime import datetime, timedelta

# d = datetime.utcnow()
# print(d)
# s = datetime.fromtimestamp(1673863025)
# print(s)
# b = d + timedelta(minutes=20)
# print(b)
# # print(datetime("2023-01-16 05:19:59.301863"))

# ddd = datetime.fromisoformat("2023-01-16 05:19:59")
# print(ddd)
# c = datetime(2023, 2, 16, 10, 57, 5)
# print(c)

# name: str = "name,game"
# n = name.split(",")
# print(n)
# dont = {"sort": "derek", "man": "chester", "skip": "mae"}
# exclude = ["sort", "skip", "page", "limit"]
# for data in exclude:
#     if data in dont.keys():
#         del dont[data]

# print(dont)

# for k, v in dont.items():
#     exec(k + "=v")
#     print(f"{k} = {v}")


# hello.py
#  hi = "kello"


# from hashlib import blake2b
# from hmac import compare_digest

# SECRET_KEY = b"well cant say more than this "
# AUTH_SIZE = 16


# def sign(cookie: str):
#     h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
#     data = cookie.encode(("utf-8"))
#     h.update(data)
#     return h.hexdigest()


# def verify(cookie, sig):
#     good_sig = sign(cookie)
#     print(compare_digest(good_sig, sig))
#     return compare_digest(good_sig, sig)


# print(sign("hello"))
# print(verify(cookie="helo", sig="f1a51ad5868278758e92a5e75f3165d4"))
# from typing import TypedDict, Any


# class TypeDict(TypedDict):
#     pass


# def pick(T: TypeDict, keys: list[str]) -> TypeDict:
#     new_dict = {key: T[key] for key in keys}
#     return TypeDict(**new_dict)


# class ResponseT(TypedDict):
#     message: str
#     data: dict[str, Any]
#     success_status: bool


# x = pick(ResponseT, ["message"])


# f: x = {"hello", "hi"}

# print(f)


def getDict(select: str) -> tuple[dict | None, dict | None]:
    if select is None:
        return {}, {}
    get_list = [field.strip() for field in select.split(",")]
    add_field = [field for field in get_list if not field.startswith("-")]
    remove_field = [field[1:] for field in get_list if field.startswith("-")]
    return add_field, remove_field


print(getDict("-hello, derek, -mae, -age, -nude"))

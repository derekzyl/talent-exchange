import random
import string
import uuid
from datetime import datetime
from typing import Literal

# initializing size of string
N: Literal[10] = 10

# using random.choices()
# generating random strings
res: str = "".join(random.choices(string.ascii_lowercase + string.digits, k=N))


me: uuid.UUID = uuid.uuid4()
j: str = str(me)
k: list[str] = j.split("-")

l: str = "".join(k)
g = datetime.utcnow()
hh = g.strftime("%Y%m%d%H%M%S")


def id_gen() -> str:

    m: str = hh + res + l


    return m

from pydantic import BaseModel
from string import ascii_lowercase, ascii_uppercase, digits
from typing import Final
from random import choice

CHARS: Final[str] = ascii_uppercase + ascii_lowercase + digits


def UUID() -> str:
    uuid = [''.join(choice(CHARS) for _ in range(5)) for _ in range(4)]
    return '-'.join(uuid)


class Artist(BaseModel):
    name: str
    age: int
    music_genre: str
    releases: dict[str, list[str]]
    is_active: bool

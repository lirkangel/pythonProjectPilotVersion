from typing import Any

from pydantic.main import BaseModel


class AuthBody(BaseModel):
    username: str
    password: str


class AuthRequest(AuthBody):
    email: str


class AnyBody(BaseModel):
    user: Any

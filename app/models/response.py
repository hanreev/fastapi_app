from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class BaseResponseContent(BaseModel, Generic[T]):
    status: bool
    message: str
    data: T | None = None


class ResponseContent(BaseResponseContent):
    status: bool = True


class ErrorResponseContent(BaseResponseContent):
    status: bool = False

from fastapi import HTTPException, Request, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from urllib.parse import quote


class WebBaseErrorSchema(BaseModel):
    error: bool = True
    message: str = "內部錯誤"

class Error(WebBaseErrorSchema):
    pass

class WebBaseException(Exception):
    def __init__(
        self,
        status_code: int = 500,
        error: bool = True,
        message: str = "內部錯誤",
        headers: dict[str, str] | None = {"description": quote("伺服器內部錯誤"), },
        *args,
    ) -> None:
        self.status_code = status_code
        self.error = error
        self.message = message
        self.headers = headers

    def __str__(self) -> str:
        return f"{self.status_code} | {self.error}: {self.message}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.error!r}, detail={self.message!r})"


class AttractionInternalError(WebBaseException):
    pass


class AttractionInternalErrorSchema(WebBaseErrorSchema):
    pass


def general_exception_handler(request: Request, exc: WebBaseException):
    content = WebBaseErrorSchema(error=exc.error, message=exc.message)
    return JSONResponse(
        status_code=exc.status_code, headers=exc.headers, content=content.model_dump()
    )

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

# 錯誤響應模型
class WebBaseErrorSchema(BaseModel):
    error: bool
    message: Optional[str] = None

class Error(WebBaseErrorSchema):
    pass

# 異常類
class WebBaseException(Exception):
    def __init__(
        self,
        error: bool,
        message: str,
        status_code: int = 500,
        headers: dict = None):
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

# 符合if捕獲的異常處理器
async def general_exception_handler(request: Request, exc: WebBaseException):
    content = WebBaseErrorSchema(error=exc.error, message=exc.message)
    return JSONResponse(
        status_code=exc.status_code, headers=exc.headers, content=content.model_dump()
    )

# 其他所有的異常處理器
async def internal_server_error_handler(request:Request, exc:Exception):
    return JSONResponse(
        status_code=500,
        content=WebBaseErrorSchema(error=True, message="伺服器內部錯誤").model_dump()
    )
import logging

from fastapi import Request
from fastapi.responses import JSONResponse
import jwt
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings

SECRET = settings.secret_key

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/static") or request.url.path.startswith("/attraction") or request.url.path.startswith("/api/attraction"):
            return await call_next(request)
        if request.url.path in ["/api/user/auth", "/", "/docs", "/api/mrts","/api/user/signup"]:
            return await call_next(request)
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split("Bearer ")[1]
            try:
                payload = jwt.decode(token, SECRET, algorithms=["HS256"])
                request.state.payload = payload
                logging.debug("Decoded payload: %s", request.state.payload)
                
            except jwt.exceptions.InvalidTokenError:
                print('jwt')
                return JSONResponse(
                    status_code=401,
                    content={"error": True, "message": "Invalid or expired token"}
                )
        else:
            print('else')
            return JSONResponse(
                status_code=401,
                content={"error": True, "message": "Authorization header missing"}
            )
        
        response = await call_next(request)
        return response


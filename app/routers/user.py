from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import Session, select
import pendulum
import logging

from schema import *
from database import engine
from models import *
from exceptions import *
from config import settings


SECRET = settings.secret_key

user_router = APIRouter(prefix="/user")


@user_router.post(
    "/signup",
    summary="註冊一個新的會員",
    responses={
        200: {
            "description": "註冊成功",
            "content": {
                "application/json": {
                    "example": {
                        "ok": True,
                    }
                }
            },
            "model": Success,
        },
        400: {
            "description": "註冊失敗，重複的 Email 或其他原因",
            "content": {
                "application/json": {
                    "example": {
                        "error": True,
                        "message": "註冊失敗，重複的 Email 或其他原因",
                    }
                }
            },
            "model": Error,
        },
        500: {
            "description": "伺服器內部錯誤",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "伺服器內部錯誤"}
                }
            },
            "model": Error,
        },
    },
)
async def create_user(user: UserSignUpInput):
    with Session(engine) as session:
        statement = select(User).where(User.email == user.email)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise WebBaseException(
                error=True,
                status_code=400,
                message="註冊失敗，重複的 Email 或其他原因",
            )
        try:
            new_user = User(
                email=user.email, name=user.name, password=user.password, created_at=pendulum.now(), updated_at=pendulum.now()
            )
            session.add(new_user)
            session.commit()

            return Success(ok=True)
        except Exception as e:
            logging.error(f"Error while creating user: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )


@user_router.get(
    "/auth",
    summary="取得當前的會員資訊",
    response_model=UserResponse,
    responses={
        200: {
            "description": "已登入的會員資料，null 表示未登入",
        },
    },
)
async def get_user(request: Request):
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split("Bearer ")[1]
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])

        user = User(id=payload["id"], name=payload["name"], email=payload["email"])
        response = UserResponse(data=user)

    except jwt.exceptions.InvalidTokenError:
        response = UserResponse(data=None)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    return response


@user_router.put(
    "/auth",
    summary="登入會員帳戶",
    response_model=TokenResponse,
    responses={
        200: {
            "description": "登入成功，取得有效期為七天的 JWT 加密字串",
        },
        400: {
            "description": "登入失敗，帳號或密碼錯誤或其他原因",
            "content": {
                "application/json": {
                    "example": {
                        "error": True,
                        "message": "登入失敗，帳號或密碼錯誤或其他原因",
                    }
                }
            },
            "model": Error,
        },
        500: {
            "description": "伺服器內部錯誤",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "伺服器內部錯誤"}
                }
            },
            "model": Error,
        },
    },
)
async def signin_user(user: UserSingIn):
    with Session(engine) as session:
        statement = select(User).where(User.email == user.email)
        existing_user = session.exec(statement).first()

        if existing_user is None or existing_user.password != user.password:
            raise WebBaseException(
                error=True,
                status_code=400,
                message="登入失敗，帳號或密碼錯誤或其他原因",
            )

        try:
            user_data = {
                "id": str(existing_user.id),
                "name": existing_user.name,
                "email": existing_user.email,
            }
            encoded_jwt = jwt.encode(
                {
                    "exp": pendulum.now()
                    .add(days=7)
                    .int_timestamp,  # 設定過期時間為7天的Unix時間戳
                    **user_data,
                },
                SECRET,
                algorithm="HS256",
            )

            return TokenResponse(token=encoded_jwt)
        except Exception as e:
            print(f"Error while encoding JWT: {e}")
            raise WebBaseException(
                error=True,
                status_code=500,
                message="伺服器內部錯誤",
            )

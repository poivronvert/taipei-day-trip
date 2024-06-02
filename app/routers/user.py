from typing import List

from fastapi import APIRouter



user_router = APIRouter()

@user_router.post("/user")
def get_user():
    pass

@user_router.get("/user/auth")
def get_user():
    pass

@user_router.put("/user/auth")
def get_user():
    pass
from typing import List

from fastapi import APIRouter



order_router = APIRouter()

@order_router.get("/order")
def get_order():
    pass
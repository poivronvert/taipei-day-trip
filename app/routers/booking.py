from typing import List

from fastapi import APIRouter



booking_router = APIRouter()

@booking_router.get("/booking")
def get_booking():
    pass
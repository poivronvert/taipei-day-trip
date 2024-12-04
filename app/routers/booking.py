from typing import List
import logging
import jwt
import os

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel import Session, select
from dotenv import load_dotenv

from schema import *
from exceptions import *
from database import engine
from models import *
from routers.user import get_user
from crud import delete_booking_from_db, add_booking_to_db, check_attraction_exist, get_all_bookings, get_booking_by_id

logging.basicConfig(level=logging.DEBUG)

booking_router = APIRouter(prefix="/api/booking")

@booking_router.get("")
async def get_all_bookings(request: Request):
    try:
        user_id = request.state.payload["user_id"]
        result = await get_all_bookings(user_id)
        return BookingsOverviewResponse(data=result)
    
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=403, detail="未登入系統")

    except Exception as e:
        logging.error(e, exc_info=True)
        return HTTPException(status_code=500, detail="伺服器內部錯誤")
    
@booking_router.get("/get?booking_id={booking_id}")
async def get_booking(request: Request, booking_id: str):
    try:
        user_id= request.state.payload["user_id"]
        booking_result = await get_booking_by_id(user_id, booking_id)
        if booking_result:
            return booking_result
        
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=403, detail="未登入系統")

    except Exception as e:
        logging.error(e, exc_info=True)
        return Error(error=True, message="伺服器內部錯誤")

@booking_router.post("/create")
async def create_booking(request: Request, booking_input: BookingInfo):
    try:
        user_id = request.state.payload["user_id"]
        attraction_id = booking_input.attractionId
        date = booking_input.date
        time = booking_input.time
        price = booking_input.price

        # 檢查景點是否存在
        attraction = await check_attraction_exist(attraction_id)
        if not attraction:
            raise ValueError("景點不存在")
        
        # 檢查時間與價格是否匹配
        if (time == "morning" and price != 2000) or (time == "afternoon" and price != 2500):
            raise ValueError("價格不正確")
        
        # 新增預定
        result = await add_booking_to_db(user_id, attraction_id, date, time, price)
        if result is True:
            return Success(ok=True)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=403, detail="未登入系統")
    
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")


@booking_router.delete("/delete?booking_id={booking_id}")
async def delete_booking(request: Request, booking_id: str):
    try:
        print(request.state.payload)
        user_id = request.state.payload["user_id"]
        result = await delete_booking_from_db(user_id, booking_id)
        if result:
            return Success(ok = True)
    
    # if missing user_id or booking_id or booking not found
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # if database error
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # if user is not logged in
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=403, detail="未登入系統")
    
    # if other error
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")

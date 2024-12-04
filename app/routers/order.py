import os
import json
import urllib.request as req
import time
import random
import logging

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from schema import Order, OrderInfo, Success
from fastapi.security import OAuth2PasswordBearer
from crud import add_order_to_db, get_order_by_id

order_router = APIRouter(prefix="/api/order")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")
load_dotenv()
key = os.getenv("SECRET_KEY")
partner_key = os.getenv("PARTNER_KEY")
tap_pay_url = os.getenv("TAP_PAY_URL")
merchant_id = os.getenv("MERCHANT_ID")


@order_router.post('')
async def order(orderInfo: OrderInfo, request: Request):
    def generate_order_id():
        timestamp = int(time.time() * 1000)  # 毫秒級時間戳
        rand_num = random.randint(1000, 9999)  # 四位隨機數
        return f"ORD{timestamp}{rand_num}"

    payment_info = {
        "prime": orderInfo.prime,
        "partner_key": partner_key,
        "amount": orderInfo.order.price,
        "merchant_id": merchant_id,
        "details": "TapPay Test",
        "cardholder": {
            "phone_number": orderInfo.order.contact.phone,
            "name": orderInfo.order.contact.name,
            "email": orderInfo.order.contact.email
        },
        "remember": False
    }

    # 將支付信息轉換為 JSON 字符串
    data = json.dumps(payment_info).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "x-api-key": partner_key
    }


    fetch_url = req.Request(tap_pay_url, data = data, headers = headers)
    try: 
        with req.urlopen(fetch_url) as response:
            response_data = response.read().decode("utf-8")
            response_json = json.loads(response_data)

            if response_json["status"] == 0:
                order_number = generate_order_id()
                user_id = request.state.payload["user_id"]
                result = await add_order_to_db(user_id,order_number, orderInfo)
                if result:
                    return Success(ok = True)
    except RuntimeError as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logging.error(e, exc_info=True)  
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")

@order_router.get("/{order_number}")
async def get_order(order_number: str, request: Request):
    try:
        user_id = request.state.payload["user_id"]
        result = await get_order_by_id(user_id, order_number)
        return result
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")

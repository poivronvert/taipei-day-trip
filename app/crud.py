import json
import re
import logging
from datetime import datetime

from sqlmodel import Session, select, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import exists

from database import engine
from models import Attraction, Image, Booking, Order
from schema import OrderInfo

def add_attraction(name,category,description,address,transport,mrt,lat,lng,images):
    with Session(engine) as session:
        new_attraction = Attraction(
            name=name,
            category=category,
            description=description,
            address=address,
            transport=transport,
            mrt=mrt if mrt else 'mrt-not-exist',
            lat=lat,
            lng=lng,
        )
        try:
            session.add(new_attraction)
            session.flush() 
            if True in (img is None for img in images):
                print(images)
                raise Exception("Image URL cannot be null")
            session.add_all((
                Image(url=img, attraction_id=new_attraction.id) 
                for img in images
            ))
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
       
def add_attraction_from_json(json_file):
    with open(json_file,'r') as file:
        data = json.load(file)
        attractions_data = data['result']['results']
        for _,attraction_data in enumerate(attractions_data):
            pattern = r'https:\/\/[^"]+?\.(?:jpg|JPG|png|PNG)'
            images = re.findall(pattern, attraction_data['file'])
            add_attraction(
                attraction_data['name'],
                attraction_data['CAT'],
                attraction_data['description'],
                attraction_data['address'],
                attraction_data['direction'],
                attraction_data['MRT'],
                attraction_data['latitude'],
                attraction_data['longitude'],
                images
            )

def get_booking_by_id(user_id, booking_id):
    if not booking_id:
        raise ValueError("Booking ID cannot be None or empty")

    try:
        with Session(engine) as session:
            statement = (
                select(Booking)
                .join(Attraction, Attraction.id == Booking.attraction_id)
                .where(Booking.id == booking_id, Booking.user_id == user_id)
            )
            result = session.exec(statement).first()
            booking_info = {
                "id": result.id,
                "attraction": {
                    "id": result.attraction.id,
                    "name": result.attraction.name,
                    "address": result.attraction.address,
                    "image": result.attraction.images[0],
                },
                "date": result.date,
                "time": result.time,
                "price": result.price,
            }
            return booking_info if result else None  # 返回 None 如果找不到結果
    except SQLAlchemyError as db_error:  # 限制為 SQLAlchemy 相關的例外
        logging.error(
            f"Database error while fetching booking with ID {booking_id} for user {user_id}: {db_error}",
            exc_info=True
        )
        raise RuntimeError("Failed to retrieve booking information") from db_error


def get_all_bookings(user_id):
    if user_id is None:
        raise ValueError("User ID cannot be None")
    try:
        with Session(engine) as session:
            statement = select(exists()).where(Booking.user_id == user_id)
            result = session.exec(statement).scalar()
            if result:
                query = select(Booking).join(Attraction, Attraction.id == Booking.attraction_id).where(Booking.user_id == user_id)
                booking_data = session.exec(query).all()
                return booking_data
            return None
            
    except Exception as e:
        logging.error(f"Error getting booking: {e}", exc_info=True)
        raise RuntimeError("Failed to get booking") from e

def check_attraction_exist(attraction_id):
    if attraction_id is None:
        raise ValueError("Attraction ID cannot be None")
    
    try:
        with Session(engine) as session:
            statement = select(exists()).where(Attraction.id == attraction_id)
            result = session.exec(statement).scalar()
            if result:
                return True
            return False
        
    except Exception as e:
        logging.error(f"Error checking attraction: {e}", exc_info=True)
        raise RuntimeError("Failed to check attraction") from e

def add_booking_to_db(user_id, attraction_id, date, time, price):
    if user_id is None or attraction_id is None or date is None or time is None or price is None:
        raise ValueError("User ID, attraction ID, date, time, and price cannot be None")
    try:
        with Session(engine) as session:
            new_booking = Booking(user_id=user_id, attraction_id=attraction_id, date=date, time=time, price=price)
            session.add(new_booking)
            session.commit()
            return True
    except Exception as e:
        logging.error(f"Error adding booking: {e}", exc_info=True)
        raise RuntimeError("Failed to add booking") from e

def delete_booking_from_db(user_id, booking_id):
    if not user_id or not booking_id:
        raise ValueError("User ID and Booking ID cannot be None or empty.")
    
    try:
        with Session(engine) as session:
            # 檢查是否存在該預約
            exists_query = select(exists().where(and_(Booking.id == booking_id, Booking.user_id == user_id)))
            if not session.exec(exists_query).scalar():
                raise ValueError("Booking not found.")
            
            # 獲取預約記錄並刪除
            booking_query = select(Booking).where(and_(Booking.id == booking_id, Booking.user_id == user_id))
            booking_data = session.exec(booking_query).first()
            session.delete(booking_data)
            session.commit()
            return True

    except ValueError:
        raise  # 傳遞自定義的 ValueError
    except Exception as e:
        logging.error(f"Error deleting booking: {e}", exc_info=True)
        raise RuntimeError("Failed to delete booking.") from e

def add_order_to_db(user_id,order_number, orderinfo: OrderInfo):
    try: 
        with Session(engine) as session:
            created_at = datetime.now()
            updated_at = datetime.now()
            new_order = Order(user_id=user_id, order_number=order_number, date=orderinfo.order.trip.date, time=orderinfo.order.trip.time, price=orderinfo.order.price, contact_name=orderinfo.order.contact.name, contact_email=orderinfo.order.contact.email, contact_phone=orderinfo.order.contact.phone, created_at=created_at, updated_at=updated_at)
            session.add(new_order)
            session.commit()
            return True

    except Exception as e:
        logging.error(f"Error adding order: {e}", exc_info=True)
        raise RuntimeError("Failed to add order") from e
    
def get_order_by_id(user_id, order_number):
    try:
        with Session(engine) as session:
            query = select(Order).where(Order.user_id == user_id).where(Order.order_number == order_number)
            result = session.exec(query).first()
            return result
    except Exception as e:
        logging.error(f"Error getting order: {e}", exc_info=True)
        raise RuntimeError("Failed to get order") from e

if __name__ == "__main__":  
    user_id = 1
    booking_id = 1
    print(get_booking_by_id(user_id, booking_id))
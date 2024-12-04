from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Enum


class Attraction(BaseModel):
    id: int | None 
    name: str 
    category: str
    description: str 
    address: str 
    transport: str 
    mrt: str 
    lat: str
    lng: str
    images: list[str]

class AttractionOut(BaseModel):
    nextPage:int | None
    data: list[Attraction]

class AttractionIdOut(BaseModel):
    data: Attraction

class User(BaseModel):
    id: int = Field(..., example='1')
    name: str = Field(..., example='ply@ply.com')
    email: str = Field(..., example='12345678')

class UserResponse(BaseModel):
    data: User

class TokenResponse(BaseModel):
    token: str =Field(description='包含 JWT 加密字串',nullable=False, example='a21312xzDSADAsadasd8u32klKDFuSAD')

class UserSignUpInput(BaseModel):
    name: str = Field(..., example='彭彭彭')
    email: str = Field(..., example='ply@ply.com')
    password: str = Field(..., example='12345678')

class UserSingIn(BaseModel):
    email: str = Field(..., example='ply@ply.com')
    password: str = Field(..., example='12345678')

class BookingInfo(BaseModel):
	attractionId: int
	date: date
	time: Literal["morning", "afternoon"]
	price: int

	@field_validator("date")
	def date_must_be_in_the_future(bookingDate):
		if bookingDate <= date.today():
			raise ValueError("Date must be after today")
		return bookingDate

class BookingsOverviewResponse(BaseModel):
    data: list[BookingInfo]
    
class Contact(BaseModel):
    name: str
    email: str
    phone: str

class AttractionInfo(BaseModel):
	id: int
	name: str
	address: str
	image: str
     
class Trip(BaseModel):
	attraction: AttractionInfo
	date: date
	time: Literal["morning", "afternoon"]

	@field_validator("date")
	def date_must_be_in_the_future(bookingDate):
		if bookingDate <= date.today():
			raise ValueError("Date must be after today")
		return bookingDate

class Order(BaseModel):
    price:Literal[1000, 2000] = Field(...,examples="2000")
    trip: Trip
    contact:Contact

class OrderInfo(BaseModel):
    prime:str = Field(...,examples="前端從第三方金流 TapPay 取得的交易碼")
    order:Order 

class Success(BaseModel):
    ok: bool
from datetime import datetime
from typing import List, Optional, Literal
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, TEXT, Sequence
import uuid

class Attraction(SQLModel, table=True):
    __tablename__ = 'attractions'

    id: int = Field(primary_key=True, default=None)
    name: str = Field(unique=True, index=True)
    category: str
    description: str = Field(sa_column=Column(TEXT))
    address: str 
    transport: str = Field(sa_column=Column(TEXT))
    mrt: str = Field(index=True)
    lat: str
    lng: str

    images: List["Image"] = Relationship(back_populates="attraction")

class Image(SQLModel, table=True):
    __tablename__ = 'images'

    id: int = Field(primary_key=True, default=None)
    url: str = Field(nullable=True)
    
    attraction_id: int = Field(foreign_key="attractions.id")
    attraction: Attraction = Relationship(back_populates="images")

class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int = Field(primary_key=True, default=None)
    name: str 
    email: str = Field(index=True)
    password: str
    created_at: datetime
    updated_at: datetime

class Booking(SQLModel, table=True):
    __tablename__ = 'bookings'

    id: int = Field(primary_key=True ,default=None)
    date: datetime
    time: str
    price: int

    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship()
    attraction_id: int = Field(foreign_key="attractions.id")
    attraction: Attraction = Relationship()
    
class Order(SQLModel, table=True):
    __tablename__ = 'orders'

    id: int = Field(primary_key=True, default=None)
    order_number: str
    date: datetime
    time: str
    price: int
    contact_name: str
    contact_email: str
    contact_phone: str
    created_at: datetime
    updated_at: datetime

    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship()
    attraction_id: int = Field(foreign_key="attractions.id")
    attraction: Attraction = Relationship()

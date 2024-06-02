from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, TEXT

__all__ = [
    "Attraction",
    "Image",
]

class AttractionBase(SQLModel, table=True):
    __tablename__ = 'attraction'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    category: str
    description: str = Field(sa_column=Column(TEXT))
    address: str 
    transport: str = Field(sa_column=Column(TEXT))
    mrt: str = Field(index=True)
    lat: str
    lng: str

    images: List["Image"] = Relationship(back_populates="attraction")

class Image(SQLModel, table=True):
    __tablename__ = 'image'

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(nullable=True)
    
    attraction_id: Optional[int] = Field(default=None, foreign_key="attraction.id")
    attraction: AttractionBase = Relationship(back_populates="images")


# class DbUser(Base):
#     __tablename__="user"
    
#     id: Mapped[intpk]
#     name:Mapped[str]
#     email:Mapped[str]
#     password:Mapped[str]
#     def __repr__(self):
#         return f"<User(id={self.id}, name={self.name}, email={self.email}, password={self.password})>"

# class DbBooking(Base):
#     __tablename__="booking"
    
#     id: Mapped[intpk]
#     date:Mapped[datetime.date]
#     time:Mapped[datetime.time]
#     price:Mapped[int]
#     user_id=mapped_column(ForeignKey("user.id"), nullable=False)
#     def __repr__(self):
#         return f"<Booking(id={self.id}, date={self.date}, time={self.time}, price={self.price}, user_id={self.user_id})>"    




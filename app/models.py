from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, TEXT

__all__ = [
    "AttractionBase",
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




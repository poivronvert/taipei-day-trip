from pydantic import BaseModel

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
    nextPage:int
    data: list[Attraction]

class AttractionIdOut(BaseModel):
    data: Attraction
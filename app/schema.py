from pydantic import BaseModel, EmailStr, Field

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
    email: EmailStr = Field(..., example='12345678')

class UserResponse(BaseModel):
    data: User

class TokenResponse(BaseModel):
    token: str

class UserSignUpInput(BaseModel):
    name: str = Field(..., example='彭彭彭')
    email: EmailStr = Field(..., example='ply@ply.com')
    password: str = Field(..., example='12345678')

class UserSingIn(BaseModel):
    email: EmailStr
    password: str

class Success(BaseModel):
    ok: bool
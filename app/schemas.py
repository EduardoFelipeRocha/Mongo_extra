from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from bson import ObjectId


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    age: int = Field(..., ge=0)
    is_active: bool = True


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=80)
    email: Optional[EmailStr]
    age: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool]


class UserInDB(UserBase):
    id: str

    class Config:
        from_attributes = True

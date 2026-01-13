from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.schema.book_schema import BookResponse as Book


# Base
class UserBase(BaseModel):
    username: str
    email: str


# Create
class UserCreate(UserBase):
    password: str


# Response
class UserResponse(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

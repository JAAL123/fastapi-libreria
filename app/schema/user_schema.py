from pydantic import BaseModel
from typing import List, Optional


# Base
class UserBase(BaseModel):
    name: str
    email: str


# Create
class UserCreate(UserBase):
    hashed_password: str


# Response
class UserResponse(UserBase):
    id: int
    is_active: bool
    borrowed_books: List[BookResponse] = []

    class Config:
        from_attributes = True

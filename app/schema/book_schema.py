from pydantic import BaseModel
from typing import List, Optional
from app.schema.author_schema import AuthorResponse as Author


class BookBase(BaseModel):
    title: str
    year: int


class BookCreate(BookBase):
    author_id: int


class BookResponse(BookBase):
    id: int
    author_id: int
    author: Author

    class Config:
        from_attributes = True


class BookInfo(BaseModel):
    id: int
    title: str
    year: int
    author: Author

    class Config:
        from_attributes = True

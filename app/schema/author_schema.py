from pydantic import BaseModel
from typing import List, Optional

# Base


class AuthorBase(BaseModel):
    name: str
    biografy: Optional[str] = None


# Create


class AuthorCreate(AuthorBase):
    pass


# Response
class AuthorResponse(AuthorBase):
    id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

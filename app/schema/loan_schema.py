from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LoanBase(BaseModel):
    book_id: int
    user_id: int
    loan_date: datetime


class Loan(LoanBase):
    id: int
    loan_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        from_attributes = True

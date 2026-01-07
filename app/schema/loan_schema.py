from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schema.book_schema import BookResponse as Book, BookInfo


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


class MyLoanResponse(BaseModel):
    id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    book: BookInfo

    class Config:
        from_attributes = True

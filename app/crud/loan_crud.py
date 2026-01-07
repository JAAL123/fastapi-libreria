from sqlalchemy.orm import Session
from app.models.loan_model import Loan


def get_loans_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    loans = (
        db.query(Loan).filter(Loan.user_id == user_id).offset(skip).limit(limit).all()
    )
    if not loans:
        return None
    return loans

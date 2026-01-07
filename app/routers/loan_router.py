from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud import loan_crud
from app.schema import loan_schema
from app.schema import user_schema
from app.dependecies import get_db, get_current_user


router = APIRouter(
    prefix="/loans",
    tags=["Loans"],
)


@router.get("/my-loans", response_model=List[loan_schema.MyLoanResponse])
def get_my_loans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
):
    loans = loan_crud.get_loans_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit, active_only=active_only
    )
    if not loans:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User has no loans"
        )
    return loans

from sqlalchemy.orm import Session, joinedload
from app.models.loan_model import Loan
from app.models.book_model import Book


def get_loans_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
):
    # Query para obtener los préstamos del usuario
    query = (
        db.query(Loan)
        .options(joinedload(Loan.book).joinedload(Book.author))
        .filter(Loan.user_id == user_id)
    )

    # si esta activo solo se traen los que no han sido devueltos
    if active_only:
        query = query.filter(Loan.return_date.is_(None))

    # aplicar paginacion
    loans = query.offset(skip).limit(limit).all()

    if not loans:
        return None
    return loans

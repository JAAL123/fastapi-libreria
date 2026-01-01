from sqlalchemy.orm import Session
from app.models.user_model import User
from app.core.security import get_password_hash
from app.schema import user_schema


def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email, username=user.username, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

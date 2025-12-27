from sqlalchemy.orm import Session
from app.models.author_model import Author
from app.schema import author_schema


def create_author(db: Session, author: author_schema.AuthorCreate):
    db_author = Author(name=author.name, biografy=author.biografy)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Author).offset(skip).limit(limit).all()

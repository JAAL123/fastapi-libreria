from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    year = Column(Integer)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    author = relationship("Author", back_populates="books")
    owner = relationship("User", back_populates="borrowed_books")

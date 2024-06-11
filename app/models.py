from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class Library(Base):
    __tablename__ = "libraries"

    library_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    address = Column(String(255))

    books = relationship("Book", back_populates="library")
    members = relationship("Member", back_populates="library")
    librarians = relationship("Librarian", back_populates="library")


class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255))
    ISBN = Column(String(255))
    publication_year = Column(Integer)
    is_available = Column(Boolean, default=True)
    library_id = Column(Integer, ForeignKey("libraries.library_id"))

    library = relationship("Library", back_populates="books")
    transactions = relationship("Transaction", back_populates="book")


class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    address = Column(String(255))
    phone_number = Column(String(255))
    library_id = Column(Integer, ForeignKey("libraries.library_id"))

    library = relationship("Library", back_populates="members")
    transactions = relationship("Transaction", back_populates="member")


class Librarian(Base):
    __tablename__ = "librarians"

    librarian_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    address = Column(String(255))
    phone_number = Column(String(255))
    library_id = Column(Integer, ForeignKey("libraries.library_id"))

    library = relationship("Library", back_populates="librarians")


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.book_id"))
    member_id = Column(Integer, ForeignKey("members.member_id"))
    issue_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="transactions")
    member = relationship("Member", back_populates="transactions")

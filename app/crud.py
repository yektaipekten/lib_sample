from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# Add these functions to crud.py


def create_book(db: Session, book: schemas.BookCreate, library_id: int):
    book_data = book.dict()
    book_data.pop("library_id", None)  # library_id anahtarını çıkarıyoruz, varsa
    db_book = models.Book(**book_data, library_id=library_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.book_id == book_id).first()


def delete_book(db: Session, book_id: int):
    db.query(models.Book).filter(models.Book.book_id == book_id).delete()
    db.commit()


def create_member(db: Session, member: schemas.MemberCreate, library_id: int):
    member_data = member.dict()
    member_data.pop("library_id", None)  # library_id anahtarını çıkarıyoruz, varsa
    db_member = models.Member(**member_data, library_id=library_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.member_id == member_id).first()


def issue_book(db: Session, book_id: int, member_id: int):
    db_transaction = models.Transaction(book_id=book_id, member_id=member_id)
    db.query(models.Book).filter(models.Book.book_id == book_id).update(
        {"is_available": False}
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def return_book(db: Session, book_id: int, member_id: int):
    db_transaction = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.book_id == book_id,
            models.Transaction.member_id == member_id,
        )
        .order_by(models.Transaction.issue_date.desc())
        .first()
    )
    if db_transaction:
        db_transaction.return_date = datetime.utcnow()
        db.query(models.Book).filter(models.Book.book_id == book_id).update(
            {"is_available": True}
        )
        db.commit()
        db.refresh(db_transaction)
    return db_transaction


def get_library(db: Session, library_id: int):
    return (
        db.query(models.Library).filter(models.Library.library_id == library_id).first()
    )


def get_libraries(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Library).offset(skip).limit(limit).all()


def create_library(db: Session, library: schemas.LibraryCreate):
    db_library = models.Library(**library.dict())
    db.add(db_library)
    db.commit()
    db.refresh(db_library)
    return db_library

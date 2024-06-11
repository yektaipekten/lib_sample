from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class LibraryBase(BaseModel):
    name: str
    address: str


class LibraryCreate(LibraryBase):
    pass


class Library(LibraryBase):
    library_id: int
    books: List["Book"] = []
    members: List["Member"] = []
    librarians: List["Librarian"] = []

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    author: str
    ISBN: str
    publication_year: int
    is_available: bool


class BookCreate(BookBase):
    library_id: int


class Book(BookBase):
    book_id: int
    library_id: int

    class Config:
        from_attributes = True


class MemberBase(BaseModel):
    name: str
    address: str
    phone_number: str


class MemberCreate(MemberBase):
    library_id: int


class Member(MemberBase):
    member_id: int
    library_id: int

    class Config:
        from_attributes = True


class LibrarianBase(BaseModel):
    name: str
    address: str
    phone_number: str


class LibrarianCreate(LibrarianBase):
    library_id: int


class Librarian(LibrarianBase):
    librarian_id: int
    library_id: int

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    book_id: int
    member_id: int
    issue_date: datetime
    return_date: Optional[datetime] = None


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    transaction_id: int

    class Config:
        from_attributes = True

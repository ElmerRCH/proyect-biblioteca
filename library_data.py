from pydantic import BaseModel
from typing import List,Optional

# Esquemas de datos
class User(BaseModel):

    username: str
    email: str
    password: str
    

class Book(BaseModel):
    title: str
    author: str
    genre: str
    year: int
    copies_available: int

class Transaction(BaseModel):
    user_id: str
    book_id: str
    transaction_type: str 
    transaction_date: str

class BookResponse(BaseModel):
    book_id: str
    title: str
    author: str
    genre: str
    year: int
    copies_available: int

class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str

class TransactionResponse(BaseModel):
    transaction_id: str
    user_id: str
    book_id: str
    transaction_type: str
    transaction_date: str

class BookListResponse(BaseModel):
    books: List[BookResponse]

class UserListResponse(BaseModel):
    users: List[UserResponse]

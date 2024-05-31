from library_data import *
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException, Form, Response

app = FastAPI()

db_users = []
db_books = []

client = MongoClient('mongodb://localhost:27017/')
db = client['biblioteca']
users_collection = db['users']

@app.get("/")
async def root(response: Response = Response()):
    response.status_code = 403
    return 'hola'

@app.post("/users/", response_model=User)
def create_user(user: User):
    db_users.append(user)
    return user

@app.get("/users/", response_model=List[User])
def read_users():
    return db_users

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    for user in db_users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Rutas para operaciones CRUD de libros
@app.post("/books/", response_model=Book)
def create_book(book: Book):
    db_books.append(book)
    return book

@app.get("/books/", response_model=List[Book])
def read_books():
    return db_books

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int):
    for book in db_books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")
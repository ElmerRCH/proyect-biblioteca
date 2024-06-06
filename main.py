from library_data import *
from .routes import usuarios
from models.usuario import User
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from fastapi import FastAPI, HTTPException, Response

app = FastAPI()
app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])

db_users = []
db_books = []

client = MongoClient('mongodb://mongodb:27017')
db = client['biblioteca']
users_collection = db['usuarios']

@app.get("/")
async def root(response: Response = Response()):
    response.status_code = 403
    return 'hola'

@app.get("/check-mongodb-connection")
def check_mongodb_connection():
    try:
        client.admin.command("ping")
        return {"message": "Conexión exitosa a MongoDB"}
    except ConnectionFailure:
        raise HTTPException(status_code=500, detail="Error al conectar a MongoDB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""@app.post("/users/")
def create_user(user: User):
   # Verifica si el usuario ya existe
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="El usuario con este email ya existe")

    # Convertir el modelo de usuario a un diccionario y guardar en MongoDB
    user_dict = user.dict()
    _ = users_collection.insert_one(user_dict)
    

    return 'echo'

"""

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
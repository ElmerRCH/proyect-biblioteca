from pymongo import MongoClient
from fastapi import APIRouter, HTTPException, Depends
from models.token import Token, create_access_token, verify_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.book import BookCreate,BookInDB
from enums.connection import Conection

router = APIRouter()

client = MongoClient(Conection.URL.value)

db = client['biblioteca']
books_collection = db['books']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register/")
def crear_usuario(book: BookCreate):
    
    if books_collection.find_one({"titulo": book.titulo}):
        raise HTTPException(status_code=400, detail="El libro ya existe")
    
    new_book = BookInDB(
        titulo=book.titulo,
        autor=book.autor,
        editorial=book.editorial,
        año_publicacion=book.año_publicacion,
        genero=book.genero,
        descripcion=book.descripcion,
        estado=book.estado
    )
    books_collection.insert_one(new_book.dict())

    return 'echo'
    
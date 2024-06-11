import requests
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
bibliotecario_collection = db['bibliotecarios']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register/")
def register_book(book: BookCreate,token: str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    bibliotecario = bibliotecario_collection.find_one({"email": token_data.email})
    
    if bibliotecario is None:
        raise credentials_exception
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


@router.get("/llenar/")
def fake_db():
    
    response = requests.get('https://www.googleapis.com/books/v1/volumes/s1gVAAAAYAAJ')
    print(response)
    
    """ new_book = BookInDB(
        titulo=book.titulo,
        autor=book.autor,
        editorial=book.editorial,
        año_publicacion=book.año_publicacion,
        genero=book.genero,
        descripcion=book.descripcion,
        estado=book.estado
    )
    books_collection.insert_one(new_book.dict())"""
    
    return 'echo'
    
    
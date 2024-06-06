from pymongo import MongoClient
from fastapi import APIRouter, HTTPException, Depends
from util.library_util import get_password_hash, verify_password
from models.token import Token, create_access_token, verify_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.bibliotecario import Bibliotecario,BibliotecarioCreate, BibliotecarioInDB
from enums.connection import Conection

router = APIRouter()

client = MongoClient(Conection.URL.value)

db = client['biblioteca']
bibliotecario_collection = db['bibliotecarios']
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register/")
def crear_usuario(bibliotecario: BibliotecarioCreate):

    if bibliotecario_collection.find_one({"email": bibliotecario.email}):
        raise HTTPException(status_code=400, detail="El bibliotecario con este email ya existe")
    hashed_password = get_password_hash(bibliotecario.hashed_password)
    
    new_bibliotecario = BibliotecarioInDB(
        username = bibliotecario.username,
        email = bibliotecario.email,
        hashed_password = hashed_password,
        )
    
    print('new_bibliotecario::::',new_bibliotecario)
    bibliotecario_collection.insert_one(new_bibliotecario.dict())

    return 'echo'
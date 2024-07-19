from pymongo import MongoClient
from fastapi import APIRouter, HTTPException, Depends
from util.library_util import get_password_hash, verify_password,authenticate
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
def crear_bibliotecario(bibliotecario: BibliotecarioCreate):
    
    if bibliotecario_collection.find_one({"email": bibliotecario.email}):
        raise HTTPException(status_code=400, detail="El bibliotecario con este email ya existe")
    hashed_password = get_password_hash(bibliotecario.password)
    
    new_bibliotecario = BibliotecarioInDB(
        username = bibliotecario.username,
        email = bibliotecario.email,
        password = hashed_password,
        )
    
    bibliotecario_collection.insert_one(new_bibliotecario.dict())

    return 'echo'


@router.post("/auth")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    #username es gmail
    bibliotecario = authenticate(form_data.username, form_data.password,bibliotecario_collection)
    if not bibliotecario:
        raise HTTPException(
            status_code=401,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token({"sub": bibliotecario['email']})
    return {"access_token": access_token, "token_type": "bearer"}
    
from pymongo import MongoClient
from fastapi import APIRouter, HTTPException, Depends
from models.token import Token, create_access_token, verify_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from util.library_util import get_password_hash, verify_password,authenticate
from models.usuario import User, UserCreate, UserInDB
from enums.connection import Conection

router = APIRouter()

client = MongoClient(Conection.URL.value)

db = client['biblioteca']
users_collection = db['usuarios']
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register/")
def crear_usuario(user: UserCreate):

    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="El usuario con este email ya existe")
    hashed_password = get_password_hash(user.password)
    new_user = UserInDB(username=user.username, email=user.email, hashed_password=hashed_password)
    users_collection.insert_one(new_user.dict())

    return 'echo'
    
@router.post("/auth")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print('llego...........')
    #username es gmail
    user = authenticate(form_data.username, form_data.password,users_collection)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token({"sub": user['email']})
    return {"access_token": access_token, "token_type": "bearer"}
    

@router.get("/check/me")
def read_users_me(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    # user = client.get(token_data.email)
    user = users_collection.find_one({"email": token_data.email})
    if user is None:
        raise credentials_exception
    
    return {'user':user['hashed_password']}
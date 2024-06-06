from pymongo import MongoClient
from fastapi import APIRouter, HTTPException, Depends
from ..models.token import Token, create_access_token, verify_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..models.usuario import User, UserCreate, UserInDB, get_password_hash, verify_password
from ..enums.connection import Conection

router = APIRouter()

client = MongoClient(Conection.URL.value)

db = client['biblioteca']
users_collection = db['usuarios']
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/usuarios/", response_model=User)
def crear_usuario(user: UserCreate):
    if user.email in client:
        raise HTTPException(status_code=400, detail="El usuario con este email ya existe")
    hashed_password = get_password_hash(user.password)
    new_user = UserInDB(username=user.username, email=user.email, hashed_password=hashed_password)
    client[user.email] = new_user
    return new_user

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(email: str, password: str):
    user = client.get(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

@router.get("/usuarios/me", response_model=User)
def read_users_me(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    user = client.get(token_data.email)
    if user is None:
        raise credentials_exception
    return user
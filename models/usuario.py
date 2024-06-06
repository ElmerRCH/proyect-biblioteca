from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserInDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

class User(BaseModel):

    #username: str
    email: str
    password: str
    
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

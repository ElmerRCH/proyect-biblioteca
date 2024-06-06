from pydantic import BaseModel, EmailStr

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
    


from pydantic import BaseModel, EmailStr
from datetime import datetime

class Bibliotecario(BaseModel):

    #username: str
    email: str
    password: str
    
class BibliotecarioCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    date_of_admission = datetime
    
class UserInDB(BibliotecarioCreate):
   pass # se hereda la clase BibliotecarioCreate

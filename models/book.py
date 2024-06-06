from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    #id: Optional[str] = None
    titulo: str
    autor: str
    editorial: str
    año_publicacion: int
    genero: str
    descripcion: Optional[str] = None
    estado: str  # Ejemplo: "disponible", "prestado", "reservado"

class BookCreate(BaseModel):
    titulo: str
    autor: str
    editorial: str
    año_publicacion: int
    genero: str
    descripcion: Optional[str] = None
    estado: Optional[str] = "disponible"  # Estado inicial por defecto
    
class BookInDB(Book):
    pass  #se herededa book
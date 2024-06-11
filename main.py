from library_data import *
from routes import usuarios,books,bibliotecarios
from fastapi import FastAPI, Response

app = FastAPI()
app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(bibliotecarios.router, prefix="/bibliotecarios", tags=["bibliotecarios"])

@app.get("/")
async def root(response: Response = Response()):
    response.status_code = 403
    return 'hola'

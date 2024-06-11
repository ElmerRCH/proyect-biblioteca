import requests
import concurrent.futures
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
async def fake_db():
    
    params = {
        'q': 'python programming',
        'maxResults': 25
    }
    works = 5
    response = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)
    libros = split_list_equally(response.json()['items'], works)
    # return response.json()
    # llenar_db(libros[0])
    
    """for libro in libros:
        llenar_db(libro)
    
    return 'echo'"""
    with concurrent.futures.ProcessPoolExecutor(max_workers=works) as executor:

        _ = [executor.submit(llenar_db,libro ) for libro in libros]
        #results = [f.result() for f in concurrent.futures.as_completed(result)]
        #count_generadas = sum(results)

    return 'echo'
        
def llenar_db(libro):
    
    for data in libro:
        
        """ print('titulo:',data['volumeInfo']['title'])
        print('autor:',data['authors'])
        print('titulo:',data['publisher'])
        print('titulo:',data['publishedDate'])
        print('titulo:',data['description'])"""
        
        if not 'volumeInfo' in data:
            continue
        
        if not all(k in data['volumeInfo'] for k in ('title', 'authors', 'publisher', 'publishedDate', 'description')):
            continue
            
        new_book = BookInDB(
            titulo=data['volumeInfo']['title'],
            autor=data['volumeInfo']['authors'],
            editorial=data['volumeInfo']['publisher'],
            año_publicacion=data['volumeInfo']['publishedDate'],
            genero='',
            descripcion=data['volumeInfo']['description'],
            estado="disponible"
        )
        books_collection.insert_one(new_book.dict())
        
    return 'echo'
    
def split_list_equally(lst, num_workers=5):


    ideal_size = len(lst) // num_workers
    remainder = len(lst) % num_workers

    result = []
    start = 0

    for i in range(num_workers):
        size = ideal_size + 1 if i < remainder else ideal_size
        result.append(lst[start:start + size])
        start += size

    result = [x for x in result if x]

    return result

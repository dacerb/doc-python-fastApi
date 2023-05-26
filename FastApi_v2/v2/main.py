from fastapi import FastAPI, Body, Path, Query, status, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title = "Mi Aplicación con FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(...,
        min_length=5,
        max_length=15
    )
    overview: str = Field(...,
        min_length=15,
        max_length=55
    )
    year: int = Field(...,
        le=2022
    )
    rating: float = Field(
        ...,
        ge=1,
        le=10
    )
    category: str = Field(
        ...,
        min_length=5,
        max_length=15
    )


    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Titulo de exmp",
                "overview": "Esto es una descripcion de mas de 15",
                "year": 2022,
                "rating": 9.8,
                "category": "Accion",

            }
        }

class User(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email":"admin@mail.com",
                "password": "admin"
            }
        }


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@mail.com":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales son invalidas")

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Accións'
    },
    {
        'id': 2,
        'title': 'Avatar2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2014',
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 3,
        'title': 'Avatar3',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2019',
        'rating': 7.8,
        'category': 'Acción'
    }
]

@app.get(
    path="/",
    tags=["home"],
)
def message():
    return HTMLResponse(
        """
        <h1> Hello World</h1>
        """
    )

@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


## Path parameters  Obligatorio
@app.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=status.HTTP_200_OK)
def get_movie(id: int = Path(
    ge=1,
    le=2000
)) -> Movie:
    """
    Descripcion de la funcion
    :param id: int
    :return: item
    """
    db = Session()
    result = db.query(MovieModel).filter(
        MovieModel.id == id
    ).first()
    #for item in movies:
    #    if item['id'] == id:
    #        return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No encontrado"})

    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


## Query parameters  Obligatorio
@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=status.HTTP_200_OK)  ## para evitar sobre escritura con otros endpoints podemos añadir una barra al final al usar query paramters
def get_movies_by_category(category: str = Query(
    min_length=5,
    max_length=15
)) -> List[Movie]:   # AL indicar en la funcion que recibe un valor pero no esta indicado en el path FastApi interpreta que es un Query parameter.
    #data = [item for item in movies if item['category'] == category]
    db = Session()
    result =db.query(MovieModel).filter(
        MovieModel.category == category
    ).all()
    if not result:
        return JSONResponse(content={'message': "No se encontraron por esa categoria"}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


@app.post("/movies", tags=["movies"], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    #movies.append(movie)
    return JSONResponse(content={"message": "Se registro la pelicula"}, status_code=status.HTTP_201_CREATED)

@app.put("/movies/{id}", tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def update_movie(id: int, movie: Movie) -> dict:

    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['category'] = movie.category
            item['rating'] = movie.rating
            return JSONResponse(content={"message": "Se ha modificado la película"}, status_code=status.HTTP_200_OK)

@app.delete("/movies/{id}", tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def update_movie(id: int) -> dict:

    for item in movies:
        if item.get('id') == id:
            movies.remove(item)
            return JSONResponse(content={"message": "Se ha eliminado la pelicula"}, status_code=status.HTTP_200_OK)


@app.post(
    path="/login",
    tags=["Auth"],
    status_code=status.HTTP_200_OK

)
def login(user: User = Body(...)):

    if user.email == "admin@mail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=status.HTTP_200_OK)
from fastapi import APIRouter
from fastapi import Path, Query, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer

movie_router = APIRouter()

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


@movie_router.get("/movies", tags=["movies"], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


## Path parameters  Obligatorio
@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=status.HTTP_200_OK)
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
@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=status.HTTP_200_OK)  ## para evitar sobre escritura con otros endpoints podemos añadir una barra al final al usar query paramters
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


@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    #movies.append(movie)
    return JSONResponse(content={"message": "Se registro la pelicula"}, status_code=status.HTTP_201_CREATED)

@movie_router.put("/movies/{id}", tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(
        MovieModel.id == id
    ).first()

    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No encontrado"})


    result.title = movie.title
    result.overview = movie.overview
    result.rating = movie.rating
    result.year = movie.year
    result.category = movie.category
    db.commit()
    return JSONResponse(content={"message": "Se ha modificado la película"}, status_code=status.HTTP_200_OK)

@movie_router.delete("/movies/{id}", tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def update_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(
        MovieModel.id == id
    ).first()

    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No encontrado"})

    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Se ha eliminado la pelicula"}, status_code=status.HTTP_200_OK)

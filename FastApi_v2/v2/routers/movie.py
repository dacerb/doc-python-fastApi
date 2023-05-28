from fastapi import APIRouter
from fastapi import Path, Query, status, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from models.movie import Movie as MovieModel
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()



@movie_router.get("/movies", tags=["movies"], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies
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
    result = MovieService(db).get_movie(id)
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
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(content={'message': "No se encontraron por esa categoria"}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Se registro la pelicula"}, status_code=status.HTTP_201_CREATED)

@movie_router.put("/movies/{id}", tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def update_movie(id: int, movie: Movie) -> dict:

    db = Session()
    result = MovieService(db).get_movie(id)

    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})

    MovieService(db).update_movie(id, movie)
    return JSONResponse(content={"message": "Se ha modificado la película"}, status_code=status.HTTP_200_OK)

@movie_router.delete("/movies/{id}", tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def update_movie(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)

    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No encontrado"})

    MovieService(db).delete_movie(id)

    return JSONResponse(content={"message": "Se ha eliminado la pelicula"}, status_code=status.HTTP_200_OK)

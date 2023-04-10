from fastapi import FastAPI, Body, Path, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Mi Aplicación con FastAPI"
app.version = "0.0.1"

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

@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=status.HTTP_200_OK)
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies, status_code=status.HTTP_200_OK)


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
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content=item, status_code=status.HTTP_200_OK)

    return JSONResponse(content=[], status_code=status.HTTP_404_NOT_FOUND)


## Query parameters  Obligatorio
@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=status.HTTP_200_OK)  ## para evitar sobre escritura con otros endpoints podemos añadir una barra al final al usar query paramters
def get_movies_by_category(category: str = Query(
    min_length=5,
    max_length=15
)) -> List[Movie]:   # AL indicar en la funcion que recibe un valor pero no esta indicado en el path FastApi interpreta que es un Query parameter.
    data = [item for item in movies if item['category'] == category]
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)


@app.post("/movies", tags=["movies"], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
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
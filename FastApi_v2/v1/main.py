from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Mi Aplicación con FastAPI"
app.version = "0.0.1"


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
    tags=["home"]
)
def message():
    return HTMLResponse(
        """
        <h1> Hello World</h1>
        """
    )

@app.get("/movies", tags=["movies"])
def get_movies():
    return movies


## Path parameters  Obligatorio
@app.get("/movies/{id}", tags=["movies"])
def get_movie(id: int):
    for item in movies:
        if item['id'] == id:
            return item

    return []


## Query parameters  Obligatorio
@app.get("/movies/", tags=["movies"])  ## para evitar sobre escritura con otros endpoints podemos añadir una barra al final al usar query paramters
def get_movies_by_category(category: str, year: int):   # AL indicar en la funcion que recibe un valor pero no esta indicado en el path FastApi interpreta que es un Query parameter.
    return [item for item in movies if item['category'] == category]


@app.post("/movies", tags=["movies"])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), category: str = Body(), rating: float = Body()):
    movies.append(dict(id=id, title=title, overview=overview, year=year, rating=rating, category=category))
    return movies

@app.put("/movies/{id}", tags=['movies'])
def update_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), category: str = Body(), rating: float = Body()):

    for item in movies:
        if item['id'] == id:
            item['title'] = title
            item['overview'] = overview
            item['year'] = year
            item['category'] = category
            item['rating'] = rating
            return movies
    return movies

@app.delete("/movies/{id}", tags=['movies'])
def update_movie(id: int):

    for item in movies:
        movies.remove(item)
        return movies
    return movies
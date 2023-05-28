from models.movie import Movie as MovieModel
from fastapi.responses import JSONResponse
from schemas.movie import Movie

class MovieService():

    def __init__(self, db) -> None:
        self.db = db

    @property
    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(
            MovieModel.id == id
        ).first()
        return result

    def get_movie_by_category(self, category):
        result = self.db.query(MovieModel).filter(
            MovieModel.category == category
        ).all()
        return result

    def create_movie(self, movie) -> None:
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return None

    def update_movie(self, id, data: Movie):
        movie = self.db.query(MovieModel).filter(
            MovieModel.id == id
        ).first()

        movie.title = data.title
        movie.overview = data.overview
        movie.rating = data.rating
        movie.year = data.year
        movie.category = data.category
        self.db.commit()
        return

    def delete_movie(self, id):
        movie = self.db.query(MovieModel).filter(
            MovieModel.id == id
        ).first()

        self.db.delete(movie)
        self.db.commit()
        return
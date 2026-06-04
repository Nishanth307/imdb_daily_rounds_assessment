from flask import Blueprint
from services.movie_service import MovieService

movie_bp = Blueprint("movies", __name__)
movie_service = MovieService()

@movie_bp.route("/movies", methods=["GET"])
def get_movies():
    return movie_service.get_movies()
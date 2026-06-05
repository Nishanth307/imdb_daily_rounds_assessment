from flask import Blueprint, request
from services.movie_service import MovieService

movie_bp = Blueprint("movies", __name__)
movie_service = MovieService()


@movie_bp.route("/movies", methods=["GET"])
def get_movies():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    year = request.args.get("year")
    language = request.args.get("language")
    sort_by = request.args.get("sort_by", "release_date")
    order = request.args.get("order", "asc")

    return movie_service.get_movies(page, limit, year, language, sort_by, order)

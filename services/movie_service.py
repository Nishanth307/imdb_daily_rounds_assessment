from repositories.movie_repository import MovieRepository
from utils.response import success_response
from utils.exceptions import BadRequestException


class MovieService:
    def __init__(self):
        self.movie_repository = MovieRepository()

    def get_movies(self, page, limit, year, language, sort_by, order):
        if page <= 0:
            raise BadRequestException("page number must be greater than 0")
        if limit <= 0:
            raise BadRequestException("limit must be greater than 0")

        query = {}
        if year:
            query["release_year"] = int(year)
        if language:
            languages_list = list(set([
                language,
                language.lower(),
                language.upper(),
                language.capitalize(),
                language.title()
            ]))
            query["languages"] = {"$in": languages_list}

        sort_order = 1 if order == "asc" else -1
        skip = (page - 1) * limit
        movies = self.movie_repository.get_movies(
            query=query,
            sort_field=sort_by,
            sort_order=sort_order,
            skip=skip,
            limit=limit,
        )

        total = self.movie_repository.count_movies(query)

        for movie in movies:
            movie["_id"] = str(movie["_id"])
            release_date = movie.get("release_date")
            if release_date:
                movie["release_date"] = release_date.strftime("%Y-%m-%d")

        return success_response(
            data={"page": page, "limit": limit, "total": total, "movies": movies}
        )

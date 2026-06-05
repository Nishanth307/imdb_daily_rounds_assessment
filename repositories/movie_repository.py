from datetime import datetime

from config.database import db


class MovieRepository:
    def __init__(self):
        self.collection = db.movies

    def bulk_insert(self, movies):
        self.collection.insert_many(movies)

    def get_movies(self, query, sort_field, sort_order, skip, limit):

        movies = (
            self.collection.find(query)
            .sort(sort_field, sort_order)
            .skip(skip)
            .limit(limit)
        )

        return list(movies)

    def count_movies(self, query):
        return self.collection.count_documents(query)

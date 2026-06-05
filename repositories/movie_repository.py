from config.database import db


class MovieRepository:
    def __init__(self):
        self.collection = db.movies

    def bulk_insert(self, movies):
        self.collection.insert_many(movies)

    def get_movies(self,query, sortfield,sortorder,skip, limit):
        movies = (
            self.collection.find(query)
            .sort(sortfield, sortorder)
            .skip(skip)
            .limit(limit)
        )

        return list(movies)

    def count_movies(self, query):
        return self.collection.count_documents(query)

    

from datetime import datetime

from config.database import db


class MovieRepository:
    def __init__(self):
        self.collection = db.movies

    def bulk_insert(self, movies):
        self.collection.insert_many(movies)

    def get_movies(self, query, sort_field, sort_order, skip, limit):
        if sort_field == "release_date":
            null_placeholder = (
                datetime.max if sort_order == 1 else datetime.min
            )
            pipeline = [
                {"$match": query},
                {
                    "$addFields": {
                        "_sort_release_date": {
                            "$ifNull": ["$release_date", null_placeholder]
                        }
                    }
                },
                {"$sort": {"_sort_release_date": sort_order}},
                {"$skip": skip},
                {"$limit": limit},
                {"$project": {"_sort_release_date": 0}},
            ]
            return list(self.collection.aggregate(pipeline))

        movies = (
            self.collection.find(query)
            .sort(sort_field, sort_order)
            .skip(skip)
            .limit(limit)
        )

        return list(movies)

    def count_movies(self, query):
        return self.collection.count_documents(query)

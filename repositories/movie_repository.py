from config.database import db


class MovieRepository:
    def __init__(self):
        self.colletion = db.movies

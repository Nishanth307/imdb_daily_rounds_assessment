import os
import uuid
from repositories.movie_repository import MovieRepository
from utils.response import success_response
from utils.csv_parser import CsvParser
from config.setting import Config
from utils.exceptions import BadRequestException


class CsvUploadService:
    def __init__(self):
        self.movie_repository = MovieRepository()

    def upload_csv(self, file):
        if not file:
            raise BadRequestException("CSV file is required")

        if file.filename == "":
            raise BadRequestException("No file selected")

        if not file.filename.endswith(".csv"):
            raise BadRequestException("only csv files are allowed")

        file_name = f"{uuid.uuid4()}.csv"

        file_path = os.path.join("uploads", file_name)

        file.save(file_path)
        self.process_csv(file_path)

        return success_response(message="csv uploaded successfully")

    def process_csv(self, file_path):
        try:
            batch = []
            for movie in CsvParser.movie_parser(file_path):
                batch.append(movie)
                if len(batch) == Config.BATCH_SIZE:
                    self.movie_repository.bulk_insert(batch)
                    batch = []
            if batch:
                self.movie_repository.bulk_insert(batch)
        except ValueError as e:
            raise ValueError(f"Invalid data format: {str(e)}")

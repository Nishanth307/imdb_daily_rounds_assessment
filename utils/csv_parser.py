import csv
from datetime import datetime


class CsvParser:
    def movie_parser(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield {
                    "title": row.get("title"),
                    "language": row.get("language"),
                    "rating": float(row.get("rating") or 0),
                    "release_date": datetime.strptime(
                        row.get("release_date"), "%Y-%m-%d"
                    ).date(),
                }

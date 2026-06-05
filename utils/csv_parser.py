import ast
from datetime import datetime

from dateutil import parser

from utils.exceptions import BadRequestException


class CsvParser:
    @staticmethod
    def parse_date(date_str):
        if not date_str:
            return None

        try:
            parsed = parser.parse(date_str, dayfirst=True)
            return datetime(parsed.year, parsed.month, parsed.day)
        except Exception:
            raise BadRequestException(f"Invalid data format: {date_str}")

    @staticmethod
    def parse_int(value):
        if not value:
            return 0
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def parse_float(value):
        if not value:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def parse_languages(value):
        if not value:
            return []

        if isinstance(value, list):
            return [str(item).strip() for item in value if item]

        value_str = str(value).strip()
        if not value_str:
            return []

        # Check if it looks like a list representation (e.g. ['english','hindi'] or ["english"])
        if value_str.startswith("[") and value_str.endswith("]"):
            try:
                parsed = ast.literal_eval(value_str)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed if item]
                elif parsed:
                    return [str(parsed).strip()]
            except Exception:
                pass

        # Fallback for plain string (e.g., "English" or "English, Hindi")
        return [item.strip() for item in value_str.split(",") if item.strip()]

    @classmethod
    def transform_row(cls, row):

        release_date = cls.parse_date(row.get("release_date"))

        return {
            "budget": cls.parse_int(row.get("budget")),
            "homepage": (row.get("homepage") or None),
            "original_language": row.get("original_language"),
            "original_title": row.get("original_title"),
            "overview": row.get("overview"),
            "release_date": release_date,
            "release_year": (release_date.year if release_date else None),
            "revenue": cls.parse_int(row.get("revenue")),
            "runtime": cls.parse_int(row.get("runtime")),
            "status": row.get("status"),
            "title": row.get("title"),
            "vote_average": cls.parse_float(row.get("vote_average")),
            "vote_count": cls.parse_int(row.get("vote_count")),
            "production_company_id": cls.parse_int(row.get("production_company_id")),
            "genre_id": cls.parse_int(row.get("genre_id")),
            "languages": row.get("languages").split(",")
            if row.get("languages")
            else [],
        }

    @classmethod
    def parse(cls, filepath):

        import csv

        with open(filepath, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                yield cls.transform_row(row)

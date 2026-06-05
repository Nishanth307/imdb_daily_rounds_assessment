import ast
from datetime import datetime

from dateutil import parser

from utils.exceptions import BadRequestException


class CsvParser:
    LANGUAGE_NAMES = {
        "en": "English",
        "fr": "Français",
        "ja": "日本語",
        "it": "Italiano",
        "es": "Español",
        "ru": "Pусский",
        "de": "Deutsch",
        "fi": "suomi",
        "tr": "Türkçe",
        "sv": "svenska",
        "pl": "Polski",
        "nl": "Nederlands",
        "el": "ελληνικά",
        "hi": "हिन्दी",
        "pt": "Português",
        "ko": "한국어",
        "zh": "普通话",
        "ar": "العربية",
        "da": "Dansk",
        "no": "Norsk",
        "cs": "Český",
        "hu": "Magyar",
        "th": "ภาษาไทย",
        "he": "עִבְרִית",
        "cn": "普通话",
        "xx": "No Language",
    }

    @staticmethod
    def map_original_language(code):
        if not code:
            return None
        return CsvParser.LANGUAGE_NAMES.get(code.strip().lower())

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

        value = value.strip()

        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return parsed
            if isinstance(parsed, str):
                return [parsed]
        except Exception:
            pass

        if "|" in value:
            return [lang.strip() for lang in value.split("|") if lang.strip()]

        return [value]

    @classmethod
    def transform_row(cls, row):

        release_date = cls.parse_date(row.get("release_date"))
        original_language = row.get("original_language")
        languages = cls.parse_languages(row.get("languages") or row.get("language"))

        if not languages and original_language:
            mapped = cls.map_original_language(original_language)
            if mapped:
                languages = [mapped]

        return {
            "budget": cls.parse_int(row.get("budget")),
            "homepage": (row.get("homepage") or None),
            "original_language": original_language,
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
            "languages": languages,
        }

    @classmethod
    def parse(cls, filepath):

        import csv

        with open(filepath, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                yield cls.transform_row(row)

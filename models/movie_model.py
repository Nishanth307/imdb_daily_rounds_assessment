from dataclasses import dataclass
from datetime import datetime


@dataclass
class Movie:
    title: str
    overview: str
    original_title: str
    original_language: str
    home_page: str
    budget: str
    status: str
    runtime: int
    revenue: int
    release_date: datetime
    genre_id: int
    vote_count: int
    vote_average: float

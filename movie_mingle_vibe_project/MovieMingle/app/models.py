from dataclasses import dataclass

@dataclass
class Movie:
    id: str
    title: str
    year: int
    rating: float
    genres: list
    poster_url: str
    plot: str

@dataclass
class MovieList:
    id: str
    name: str
    description: str
    share_url: str
    created_at: str

@dataclass
class ListMovie:
    list_id: str
    movie_id: str
    added_at: str

# Placeholder for future relational database models
# from sqlalchemy import create_engine, Column, String
# # Example SQLAlchemy models
# class Movie(db.Model):
#     id = Column(String, primary_key=True)
#     title = Column(String, nullable=False)
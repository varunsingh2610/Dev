#=================================================================================================================
#=================================================================================================================

# SYSTEM MODULE
from sqlalchemy import Column, String, Numeric, Table, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

# CUSTOM MODULE
from .db_base import Base

#=================================================================================================================
#=================================================================================================================

MovieGenre = Table('MovieGenre', Base.metadata,
			 Column('id', Integer, primary_key=True, autoincrement=True),
			 Column('movie_id', Integer, ForeignKey('Movie.movie_id')),
			 Column('genre_id', Integer, ForeignKey('Genre.genre_id')))

class Genre(Base):
    """Gerne entity to store the genre of the movies"""
    __tablename__ = "Genre"
    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    name     = Column(String(500), nullable=False, unique=True)


class Movie(Base):
    """Movie entity to store the movies details having relation with genre"""
    __tablename__ = "Movie"
    movie_id   = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String(500), nullable=False, unique=True)
    director   = Column(String(500), nullable=False)
    imdb_score = Column(Numeric(2,1), nullable=False)
    popularity = Column(Numeric(4,2), nullable=False)
    genre      = relationship("Genre", secondary=MovieGenre)

class User(Base):
    """User entity to store the user details and access"""
    __tablename__ = "User"
    user_id     = Column(Integer, primary_key=True, autoincrement=True)
    username    = Column(String(50), nullable=False, unique=True)
    password    = Column(String(50), nullable=False)
    basic_auth  = Column(String(500), nullable=False)
    admin_role  = Column(Boolean, nullable=False)
    user_status = Column(String(20), nullable=True)

#=================================================================================================================
#=================================================================================================================

#=================================================================================================================
#=================================================================================================================
from .db_base import Session, engine, Base
from .movies import Movie, Genre, MovieGenre, User
#=================================================================================================================
#=================================================================================================================
Base.metadata.create_all(engine)
#=================================================================================================================
#=================================================================================================================




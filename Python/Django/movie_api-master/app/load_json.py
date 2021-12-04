
#=================================================================================================================
#=================================================================================================================

from .config import *
from .model.movies import Movie, Genre, MovieGenre
from .model.db_base import Session, engine, Base

#=================================================================================================================
#=================================================================================================================
class LoadJson():
    def handle(self):
        try:
            db = Session()
            with open(IMDB_JSON_FILEPATH, 'r') as f:
                data = json.loads(f.read())
                # print(data)
                movie_data = {}

                for movie_item in data:
                    movie_data['name']       = movie_item.get('name')
                    movie_data['popularity'] = movie_item.get('99popularity')
                    movie_data['director']   = movie_item.get('director')
                    movie_data['imdb_score'] = movie_item.get('imdb_score')
                    genre_list  = movie_item.get('genre')

                    # movie = Movie(**movie_data)
                    movie_exist = db.query(Movie).filter(Movie.name.ilike(movie_data['name'])).first()
                    movie = Movie(**movie_data)

                    if not movie_exist:

                        for genre_item in genre_list:
                            name  = genre_item.strip()
                            genre = Genre(name=name)
                            genre_exist = db.query(Genre).filter(Genre.name.ilike(name)).first()

                            if not genre_exist:
                                movie.genre.append(genre)
                                db.add(movie)
                            else:
                                db.add(movie)
                                # print(movie.name, genre.name)
                                genre = db.query(Genre).filter(Genre.name.ilike(genre.name)).first()
                                movie = db.query(Movie).filter(Movie.name.ilike(movie.name)).first()
                                movie.genre.append(genre)
                                db.add(movie)
                        # print(movie)
                        db.commit()

                    else:
                        print("Movie already exist: ", movie.name)
                        continue

        except Exception as e:
            print(e)
            db.rollback()

        finally:
            db.close()            


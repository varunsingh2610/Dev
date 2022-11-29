#!/usr/bin/python
"""
TITLE              : movie_admin.py
DESCRIPTION        : This script storing the movie data into DB.
AUTHOR             : 1. Sandip Darwade <sandipdrwde@gmail.com>
DATE CREATED       : 12/10/2018
DATE LAST MODIFIED : 12/10/2018
VERSION            : 0.1
USAGE              : 
NOTES              : 
PYTHON_VERSION     : 3.x
STATUS             : Development
"""
#=================================================================================================================
#=================================================================================================================
import falcon
import json
from collections import OrderedDict
#=================================================================================================================
from ..model.db_base import Session, engine, Base
from ..model.movies import Movie, Genre, MovieGenre, User
from ..validate_access_token import Authorize
#=================================================================================================================
#=================================================================================================================

class MovieAdmin():
    def on_get(self, req, resp):
        try:
            """
            Fetch Movies data from Database
            """
            db = Session()
            rows = db.query(Movie).all()
            output = {'movie_data': []}
            for mrow in rows:
                genre = []
                for grow in mrow.genre:
                    genre.append(grow.name)

                data = OrderedDict({"name":mrow.name,
                					"popularity":str(mrow.popularity),
                					"director":mrow.director,
                					"imdb_score":str(mrow.imdb_score),
                					"genre":genre
                				})
                output['movie_data'].append(data)

            output["Status"] = falcon.HTTP_200
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(output)

        except Exception as e:
            resp.body = json.dumps({"Status": falcon.HTTP_400, 'Error':str(e)})
            resp.status = falcon.HTTP_400
            return resp

        finally:
            db.close()


#=================================================================================================================
#=================================================================================================================

    @falcon.before(Authorize())
    def on_post(self, req, resp):
        try:
            """
            Insert movie data into database
            """
            db = Session()
            raw_json = req.stream.read()
            raw_data = json.loads(raw_json.decode("utf-8"))
            genre_list  = raw_data.pop('genre')

            movie_data = dict(name = raw_data['name'],
            				popularity = raw_data['popularity'],
            				director = raw_data['director'],
            				imdb_score = raw_data['imdb_score']
            				)
            movie_exist = db.query(Movie).filter(Movie.name.ilike(movie_data['name'].strip())).first()
            movie = Movie(**movie_data)

            if not movie_exist:

                for genre_item in genre_list:
                    name  = genre_item.strip()
                    genre = Genre(name=name)
                    genre_exist = db.query(Genre).filter(Genre.name.ilike(name.strip())).first()

                    if not genre_exist:
                        movie.genre.append(genre)
                        db.add(movie)
                    else:
                        db.add(movie)
                        movie = db.query(Movie).filter(Movie.name.ilike(movie.name.strip())).first()
                        movie.genre.append(genre_exist)
                        db.add(movie)
                # print(movie)
                output = {'Status': falcon.HTTP_200, 'Message': "Movie data saved successfully for: "+movie.name}
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(output)
                db.commit()                

            else:
                resp.body = json.dumps({"Status": falcon.HTTP_400, "Error":"Movie name already exist: "+movie.name})
                resp.status = falcon.HTTP_400
                return resp
  
        except (KeyError, ValueError) as e:
            db.rollback()
            error = "{err} field is required..!".format(err=e) 
            resp.body = json.dumps({"Status": falcon.HTTP_400, 'Error':str(error)})
            resp.status = falcon.HTTP_400

        except Exception as e:
            db.rollback()
            resp.body = json.dumps({"Status": falcon.HTTP_400, 'Error':str(e)})
            resp.status = falcon.HTTP_400
            return resp

        finally:
            db.close()


#=================================================================================================================
#=================================================================================================================

    @falcon.before(Authorize())
    def on_put(self, req, resp):
        try:
            """
            Update movie data into database
            """
            db = Session()
            raw_json = req.stream.read()
            movie_data = json.loads(raw_json.decode("utf-8"))
            genre_list  = movie_data.pop('genre')
            movie_exist = db.query(Movie).filter(Movie.name.ilike(movie_data['name'].strip())).first()

            if movie_exist:
                movie_exist.popularity = movie_data["popularity"]
                movie_exist.director = movie_data["director"]
                movie_exist.imdb_score = movie_data["imdb_score"]
                movie_exist.genre.clear()

                for genre_item in genre_list:
                    name  = genre_item.strip()
                    genre = Genre(name=name)
                    genre_exist = db.query(Genre).filter(Genre.name.ilike(name.strip())).first()

                    if not genre_exist:
                        movie_exist.genre.append(genre)
                        db.add(movie_exist)
                    else:
                        movie_exist.genre.append(genre_exist)
                        db.add(movie_exist)

                output = {'Status': falcon.HTTP_200, 'Message': "Movie data updated successfully for: "+movie_data["name"]}
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(output)
                db.commit()                

            else:
                resp.body = json.dumps({"Status": falcon.HTTP_404, "Error":"Movie name does not exist: "+movie_data["name"]})
                resp.status = falcon.HTTP_404
                return resp
  
        except (KeyError, ValueError) as e:
            db.rollback()
            error = "{err} field is required..!".format(err=e) 
            resp.body = json.dumps({"Status": falcon.HTTP_400, 'Error':str(error)})
            resp.status = falcon.HTTP_400

        except Exception as e:
            db.rollback()
            resp.body = json.dumps({"Status": falcon.HTTP_400, 'Error':str(e)})
            resp.status = falcon.HTTP_400
            return resp

        finally:
            db.close()


#=================================================================================================================
#=================================================================================================================


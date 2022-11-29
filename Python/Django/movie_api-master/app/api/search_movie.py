#!/usr/bin/python
"""
TITLE              : search_movie.py
DESCRIPTION        : This script is searching the movies based on movie name.
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

#=================================================================================================================
#=================================================================================================================

class SearchMovie():
    def on_get(self, req, resp, movie_name):
        try:
            """
            Search Movies based on movie names (case insensitive)
            """
            db = Session()
            movie = db.query(Movie).filter(Movie.name.ilike(movie_name.strip())).first()
            output = {}
            if movie:
                data = OrderedDict({"name":movie.name,
                                    "popularity":str(movie.popularity),
                                    "director":movie.director,
                                    "imdb_score":str(movie.imdb_score),
                                    "genre":[genre.name for genre in movie.genre]
                                })
                output['movie_data'] = data
                output["Status"] = falcon.HTTP_200
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(output)
            
            else:
                resp.body = json.dumps({"Status": falcon.HTTP_404, "Error":"Movie name not found: "+movie_name})
                resp.status = falcon.HTTP_404
                return resp

        except Exception as e:
            resp.body = json.dumps({"Status": falcon.HTTP_400, 'Error':str(e)})
            resp.status = falcon.HTTP_400
            return resp

        finally:
            db.close()

#=================================================================================================================
#=================================================================================================================

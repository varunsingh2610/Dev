#!/usr/bin/python
"""
TITLE              : movie_delete.py
DESCRIPTION        : This script deleting the movie data from DB.
AUTHOR             : 1. Sandip Darwade <sandipdrwde@gmail.com>
DATE CREATED       : 13/10/2018
DATE LAST MODIFIED : 13/10/2018
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
from ..model.movies import Movie, Genre, MovieGenre
from ..validate_access_token import Authorize

#=================================================================================================================
#=================================================================================================================

class DeleteMovie():

    @falcon.before(Authorize())
    def on_delete(self, req, resp, movie_name):
        try:
            db = Session()
            movie = db.query(Movie).filter(Movie.name.ilike(movie_name.strip())).first()

            if movie:
                movie.genre.clear()
                db.query(Movie).filter(Movie.name.ilike(movie_name.strip())).delete(synchronize_session=False)
                resp.body = json.dumps({"Status": falcon.HTTP_200, "Message":"Movie deleted successfully: "+movie_name})
                resp.status = falcon.HTTP_200
                db.commit()
            else:
                resp.body = json.dumps({"Status": falcon.HTTP_404, "Error":"Movie name does not found: "+movie_name})
                resp.status = falcon.HTTP_404
                return resp

        except Exception as e:
            db.rollback()
            resp.body = json.dumps({"Status": falcon.HTTP_400, 'Error':str(e)})
            resp.status = falcon.HTTP_400
            return resp

        finally:
            db.close()

#=================================================================================================================
#=================================================================================================================

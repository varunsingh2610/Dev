
#=================================================================================================================
#=================================================================================================================
import json
import falcon
from .api.movie_admin import MovieAdmin
from .api.movie_delete import DeleteMovie
from .api.search_movie import SearchMovie
from .api.create_user import CreateUser

#=================================================================================================================
#=================================================================================================================

class ApiVersion(object):
	"""API version Info"""
	def on_get(self, req, resp):
		resp.body = json.dumps({"Version": "0.0.1", "Iteration":"1", "Release Date":"14/10/2018"})
		resp.status = falcon.HTTP_200
		return resp
		
#=================================================================================================================
#=================================================================================================================

route_list = [
	dict(resource=MovieAdmin(), url='/movies'),
	dict(resource=DeleteMovie(), url='/delete/{movie_name}'),
	dict(resource=SearchMovie(), url='/search/{movie_name}'),
	dict(resource=CreateUser(), url='/user'),
	dict(resource=ApiVersion(), url='/'),

	]

#=================================================================================================================
#=================================================================================================================

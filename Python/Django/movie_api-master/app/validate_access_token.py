#!/usr/bin/python
"""
TITLE              : validate_access_token.py
DESCRIPTION        : This script validating the access token and providing the role based access control
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
import uuid
import json
from datetime import datetime
from collections import OrderedDict
import base64

#=================================================================================================================

from .model.db_base import Session, engine, Base
from .model.movies import User

#=================================================================================================================
#=================================================================================================================

# Validating the access token
class ValidateAccessToken(object):
	"""
	Validate Access Token and return True or False.
	"""
	def validate(self, access_token):
		try:
			db = Session()
			token_b64 = base64.b64decode(access_token)
			username, pwd = (token_b64.decode("utf-8")).split(":")
			query = db.query(User).filter(User.username.like(username)).filter(User.password.like(pwd))

			if query.count() == 0:
				return False
			else:
				return True

		except Exception as e:
			print(e)

		finally:
			db.close()


#=================================================================================================================
#=================================================================================================================


class Authorize(object):
	def __call__(self, req, resp, resource, params):
		try:
			db = Session()
			token_input = req.get_header('Authorization')
			if token_input and token_input.startswith("Basic"):
				token_list = token_input and token_input.split()
				
				if len(token_list) == 2:
					token = token_list[1]
				else:
					token = None

			if token is None:
				description = ('Please provide an authorization token as part of the request.')
				raise falcon.HTTPUnauthorized('Authorization token required', description)
			else:	
				token_b64 = base64.b64decode(token)
				username, pwd = (token_b64.decode("utf-8")).split(":")

				# validating usernname and pwd against database 
				query = db.query(User).filter(User.username == username).filter(User.password == pwd)
				if query.count() != 0:
					for row in query:
						if row.admin_role:
							pass
						else:
							raise Exception("Admin access is required to add, modify and delete data")
				else:
					raise Exception("Username not found")

		except Exception as e:
			description = str(e)
			raise falcon.HTTPUnauthorized('Authorization required', description)

		finally:
			db.close()

#=================================================================================================================
#=================================================================================================================
			
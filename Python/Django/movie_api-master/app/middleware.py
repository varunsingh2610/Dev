#=================================================================================================================
#=================================================================================================================

import datetime
import decimal
import json
import falcon
import logging
from logging.handlers import RotatingFileHandler
from .config import *
from .validate_access_token import ValidateAccessToken

#=================================================================================================================
#=================================================================================================================

# Application Logger
class ResponseLoggerMiddleware(object):
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	file_handler = RotatingFileHandler(LOG_FILE_PATH, LOG_FILE_MODE, 1 * 1024 * 1024, 10)
	formatter = logging.Formatter(LOG_DEBUG_FORMAT, LOG_TIMESTAMP)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)

	def process_response(self, req, resp, resource):
		self.logger.info('{0} {1} {2}'.format(req.method, req.relative_uri, resp.status))

#=================================================================================================================
#=================================================================================================================

# Content-Type validation
class RequireJSON(object):
    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable('This API only supports responses encoded as JSON.')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType('This API only supports requests encoded as JSON.')

            # print(req.headers,"\n", req.content_length, req.cookies, req.auth, req.params)
            if req.content_length == 0:
                raise falcon.HTTPBadRequest('Empty request body', 'A valid JSON request is required.')
                # raise falcon.HTTPError(falcon.HTTP_400, 'Empty request body', 'A valid JSON request is required.')

#=================================================================================================================
#=================================================================================================================

# Token authentication
class AuthMiddleware(object):
    def process_request(self, req, resp):

    	# Access free url, so that user can register for access token
        if req.url.endswith("/user"):return

        token_input = req.get_header('Authorization')
        token_type = ['Token type="Basic"']

        # Access token validation
        if token_input and token_input.startswith("Basic"):
            token_list = token_input and token_input.split()

            if len(token_list) == 2:self.token = token_list[1]
            else:self.token = None

            if self.token is None:
                description = ('Please provide an authorization token as part of the request.')
                raise falcon.HTTPUnauthorized('Authorization token required', description, token_type)

            if not ValidateAccessToken.validate(self, self.token):
                description = ('The provided auth token is not valid. Please request a new token and try again.')
                raise falcon.HTTPUnauthorized('Invalid authentication token', description, token_type)
                
        if token_input and not token_input.startswith("Basic"):
            description = ('Please provide Basic authorization token as part of the request.')
            raise falcon.HTTPUnauthorized('Basic token type is required', description, token_type)

        if not token_input:
            description = ('Please provide an authorization token as part of the request.')
            raise falcon.HTTPUnauthorized('Authorization token required', description, token_type)

#=================================================================================================================
#=================================================================================================================

# Page or url not found
class NotFoundError(object):
    def process_response(self, req, resp, resource):
        if resp.status.find('404') > -1 and resp.body is None:
            description = 'The requested URL ['+req.path+'] was not found on the server'
            raise falcon.HTTPError(falcon.HTTP_404,'URL Not Found', description)

#=================================================================================================================
#=================================================================================================================

# If method is not implemented
class MethodNotAllowed(object):
    def process_response(self, req, resp, resource):
        if resp.status.find('405') > -1 and resp.body is None:
            description = 'The requested method not allowed on the server'
            raise falcon.HTTPError(falcon.HTTP_405,'Method Not Allowed', description)

#=================================================================================================================
#=================================================================================================================

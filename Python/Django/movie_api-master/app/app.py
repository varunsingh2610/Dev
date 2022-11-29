#!/usr/bin/python
"""
TITLE              : app.py
DESCRIPTION        : This script contains falcon app process.
AUTHOR             : 1. Sandip Darwade <sandipdrwde@gmail.com>
DATE CREATED       : 11/10/2018
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

#=================================================================================================================

from .routes import route_list
from .config import *
from .load_json import LoadJson 
from .middleware import ResponseLoggerMiddleware, AuthMiddleware, RequireJSON, NotFoundError, MethodNotAllowed

#=================================================================================================================
#=================================================================================================================


# allow_origins_list=['http://localhost:5000']
# allow_all_origins=True
# from falcon_cors import CORS
# cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True, allow_credentials_all_origins=True)


def register_route(app):
    for url_route in route_list:
        url = '{prefix}{base_url}'.format(prefix='/api', base_url=url_route.pop('url'))
        app.add_route(url, url_route.pop('resource'))
        

app = application = falcon.API(middleware=[ResponseLoggerMiddleware(), AuthMiddleware(), RequireJSON(), NotFoundError(), MethodNotAllowed()])
LoadJson().handle()
# middleware=[cors.middleware,]
register_route(app)


#=================================================================================================================
#=================================================================================================================


"""
TITLE              : run.py
DESCRIPTION        : Movie application run by this file
AUTHOR             : 1. Sandip Darwade <sandipdrwde@gmail.com> 
DATE CREATED       : 11/10/2018
DATE LAST MODIFIED : 11/10/2018
VERSION            : 0.1
USAGE              : 
NOTES              : 
PYTHON_VERSION     : 3.x
"""
#=================================================================================================================
#=================================================================================================================

import sys
import logging
logging.basicConfig(stream=sys.stderr)
# sys.path.insert(0,"/var/www/html/movie_api/")
# sys.path.append("/usr/local/lib/python3.6/dist-packages")

from app.app import app, application

#=================================================================================================================
#=================================================================================================================

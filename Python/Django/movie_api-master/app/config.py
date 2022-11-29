"""
TITLE              : config.py
DESCRIPTION        : This script parse the JSON Configuration
AUTHOR             : 1. Sandip Darwade <sandipdrwde@gmail.com> 
DATE CREATED       : 11/10/2018
DATE LAST MODIFIED : 12/10/2018
VERSION            : 0.1
USAGE              : 
NOTES              : 
PYTHON_VERSION     : 3.x
"""

#=================================================================================================================
#=================================================================================================================

# SYSTEM MODULE
import configparser
import json, os

#=================================================================================================================
#=================================================================================================================

BASE_PATH = os.getcwd()
CONFIGURATION_JSON_FILEPATH = BASE_PATH+"/config/configuration.json" # Provide configuration json absolute file path
IMDB_JSON_FILEPATH = BASE_PATH+"/config/imdb.json"
MODULE = "IMDB"

config = configparser.ConfigParser()

with open(CONFIGURATION_JSON_FILEPATH, "r") as f:
    config = json.load(f)

# Database configuration
# DATABASE_USERNAME = config[MODULE]["Database"]["DB_USER"]
# DATABASE_PASSWORD = config[MODULE]["Database"]["DB_PASS"]
# DATABASE_HOST = config[MODULE]["Database"]["DB_HOST"]
# DATABASE_PORT = config[MODULE]["Database"]["DB_PORT"]
# DATABASE_NAME = config[MODULE]["Database"]["DB_NAME"]
# DATABASE_RDMS = config[MODULE]["Database"]["DB_RDMS"]
# DATABASE_API = config[MODULE]["Database"]["DB_API"]
# DATABASE_URL = DATABASE_RDMS+"+"+DATABASE_API+"://"+DATABASE_USERNAME+":"+DATABASE_PASSWORD+"@"+DATABASE_HOST+":"+DATABASE_PORT+"/"+DATABASE_NAME
DATABASE_URL = 'sqlite:///imdb.db'

LOG_LEVEL = config[MODULE]["Logger"]["LOG_LEVEL"]
LOG_FILE_PATH = config[MODULE]["Logger"]["LOG_FILE_PATH"]
LOG_FILE_MODE = config[MODULE]["Logger"]["LOG_FILE_MODE"]
LOG_INFO_FORMAT = config[MODULE]["Logger"]["LOG_INFO_FORMAT"]
LOG_DEBUG_FORMAT = config[MODULE]["Logger"]["LOG_DEBUG_FORMAT"]
LOG_TIMESTAMP = config[MODULE]["Logger"]["LOG_TIMESTAMP"]

#=================================================================================================================
#=================================================================================================================



#!/usr/bin/python3
import mysql.connector
import os
import time
import json
import logging
import re
import pymssql
import glob
import sys
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from pymongo import MongoClient
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, create_engine, select)
import datetime
from bson.json_util import dumps
gte = '2018-05-07T00:00:00'
lte = '2018-05-09T00:00:00'
# Mongo Connection
mng_client = MongoClient('10.10.10.54',
                         username='Superadmin',
                         password='admin',
                         authSource='admin')

mng_db = mng_client['demo']
db_cm = mng_db['php_test']

cursor = db_cm.find({'date': {'$gte':'2018-05-07T00:00:00','$lt': '2018-05-09T00:00:00'}}, {'_id': 0})
print(cursor)
dumps(cursor)
for document in cursor:
    print(document)
    print('yez')



    # for document in cursor:
    #     print(document)
    #     df = df.append({'date': document['date'], 'client': document['client'], 'amount': document['amount'],
    #                     'transID': document['transID'], 'serialNumber': document['serialNumber']}, ignore_index=True)
    #
    # print(df.head())
    # exit()

from sqlalchemy import MetaData, Table, create_engine, select, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pymssql
from sqlalchemy import MetaData, create_engine
import pyodbc
from sqlalchemy.orm import Session
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, create_engine, func)
from sqlalchemy import select
from datetime import datetime
import pandas as pd
from pymongo import MongoClient
from pprint import pprint
import logging
import os
import sys

db_username = 'avn_monitor'
db_password = 'Pass@123'
db_ip = '192.168.1.30'
db_name = 'Req_data'

engine = create_engine('mssql+pymssql://{0}:{1}@{2}/{3}'.
                       format(db_username, db_password,
                              db_ip, db_name), pool_pre_ping=True, pool_recycle=3600)

metadata = MetaData()
# metadata.reflect(engine, only=['php_test'])
#
# Base = automap_base(metadata=metadata)
# Base.prepare()
# session = Session(engine)
# php_test = Base.classes.php_test
# php_test.__table__.drop(engine)
php_test = Table('php_test', metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('date', String(50)),
                 Column('client', String(50)),
                 Column('amount', String(50)),
                 Column('transID', String(50), index=True),
                 Column('serialNumber', String(50)),
                 Column('created_on', DateTime(), default=datetime.now),
                 Column('updated_on', DateTime(),
                        default=datetime.now, onupdate=datetime.now)
                 )
metadata.create_all(engine)

php_test = Table('php_test', metadata,
                       autoload=True, autoload_with=engine)
s = select([php_test]).count()
print(engine.execute(s).fetchall())

s = select([func.count()]).select_from(php_test)
print(engine.execute(s).fetchall())

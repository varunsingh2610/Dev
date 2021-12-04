#!/usr/bin/env python
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



# with open('bad_lines.txt', 'w') as fp:
#     sys.stderr = fp
#     pd.read_csv('data/COP_NBK.txt', sep='^',
#                      header=None,  engine='python', error_bad_lines=False)

# metadata = MetaData()
#
# php_test = Table('php_test', metadata,
#                  Column('id', Integer(), primary_key=True),
#                  Column('date', String(50)),
#                  Column('client', String(50)),
#                  Column('amount', String(50)),
#                  Column('transID', String(50), index=True),
#                  Column('serialNumber', String(50)),
#                  Column('created_on', DateTime(), default=datetime.now),
#                  Column('updated_on', DateTime(),
#                         default=datetime.now, onupdate=datetime.now)
#                  )

# logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p', filename='practice_six.log', level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.info('The Script has started.')
# df = pd.read_csv('data/COP_NBK.txt', sep='^',
#                  header=None,  engine='python', error_bad_lines=False)
# print(df.head())
# MSSQL Connection

db_username = 'avn_monitor'
db_password = 'Pass@123'
db_ip = '192.168.1.30'
db_name = 'Req_data'

engine = create_engine('mssql+pymssql://{0}:{1}@{2}/{3}'.
                       format(db_username, db_password,
                              db_ip, db_name), pool_pre_ping=True, pool_recycle=3600)

metadata = MetaData()
mssqlTable = Table('php_test', metadata, autoload=True, autoload_with=engine)
print(mssqlTable.columns.keys())


# Base = automap_base()
# Base.prepare(engine, reflect=True)

# metadata.create_all(engine)


# Mongo Connection

# client = MongoClient('10.10.10.54',
#                      username='Superadmin',
#                      password='admin',
#                      authSource='admin')
# mng_db = client['Reconcillation']
# db_cm = mng_db['ReconDataCollection_August2018']
#
# df = pd.DataFrame(columns=['date', 'client', 'amount', 'transID', 'serialNumber'])
# cursor = db_cm.find({},{'_id': 0})
# for document in cursor:
#     df = df.append({'date': document['date'],'client': document['client'],'amount': document['amount'], 'transID': document['transID'],'serialNumber': document['serialNumber']}, ignore_index=True)
#     pprint(document)
# print(df)
#
# print(client)
# metadata.reflect(engine, only=['HDFC_Apr2018_1', 'HDFC_Apr2018_2'])
#
# Base = automap_base(metadata=metadata)
# Base.prepare()
# session = Session(engine)
#
# php_test = Base.classes.php_test
# pendingData = session.query(php_test).filter(php_test.username == "").first()
# php_test.__table__.drop(engine)


# HDFC_Apr2018_1 = Table('HDFC_Apr2018_1', metadata,
#                        autoload=True, autoload_with=engine)
# HDFC_Apr2018_1.columns.keys()
# s = select([HDFC_Apr2018_1]).limit(1)
# print(engine.execute(s).fetchall())
# metadata = MetaData()
#
php_test = Table('php_test', metadata,
                       autoload=True, autoload_with=engine)
# s = select([php_test]).count()
# print(engine.execute(s).fetchall())

s = select([func.count()]).select_from(php_test)
print(engine.execute(s).fetchall())

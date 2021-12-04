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


# #Create and configure logger
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', filename='dataProcessing.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info('The Script has started.')

# Static values
dateFormat = {'DD/MM/YYYY HH/MM': '%d/%m/%Y %H/%M',
              'DD/MM/YYYY HH/MM/SS': '%d/%m/%Y %H/%M/%S',
              'DD/MM/YYYY HH/MM/SS.milliseconds': '%Y-%m-%d %H:%M:%S.%f',
              'DD/MM/YYYY': '%d/%m/%Y',
              'DD/MM/YY': '%d/%m/%y',
              'DD/MM/YY HH:MM': '%d/%m/%y %H:%M',
              'DD-MM-YY HH:MM:SS': '%d-%m-%y %H:%M:%S',
              'YYYY-MM-DD HH:MM:SS': '%Y-%m-%d %H:%M:%S',
              'YYYY-MM-DDTHH:MM:SSZ': '%Y-%m-%dT%H:%M:%SZ',
              'YY-MM-DD HH:MM:SS': '%y-%m-%d %H:%M:%S',
              'YY-MM-DDTHH:MM:SSZ': '%y-%m-%dT%H:%M:%SZ',
              'DD-MMM-YY HH:MM:SS': '%d-%b-%y %H:%M:%S',
              'DD-MMM-YY HH:MM': '%d-%b-%y %H:%M',
              'DD-MMM-YY': '%d-%b-%y',
              'YYMMDDHHMMSS': '%y%m%d%H%M%S',
              'DDMMYYHHMM': '%d%m%y%H%M',
              'DDMMYYYYHHMM': '%d%m%Y%H%M',
              'YYMMDD': '%y%m%d',
              'YYYYMMDD': '%Y%m%d',
              'YY/MM/DD': '%y/%m/%d',
              'MM-DD-YY': '%m-%d-%y',
              'YY-MM-DD': '%y-%m-%d',
              }
filesPath = '/var/www/html/DataProcessor/assets/data'


# Static Database values
db_username = 'root'
db_password = 'Passw0rd'
db_ip = '10.10.10.54'
db_name = 'DataProcessor'

# Connection for MySQL server

engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                       format(db_username, db_password,
                              db_ip, db_name), pool_pre_ping=True, pool_recycle=3600)
logger.info('Connected to MySQL DB.')

# MySQL Server Mapping
myBase = automap_base()
myBase.prepare(engine, reflect=True)
mySession = Session(engine)
logger.info('MySQL Mapping and Session created.')

# Loading Tables from MySQL Server
tblDataProcessing = myBase.classes.tblDataProcessing
tblTemplates = myBase.classes.tblTemplates
tblDBConnection = myBase.classes.tblDBConnection


pendingData = mySession.query(tblDataProcessing).filter(
    tblDataProcessing.iDataStatus == "1").first()
if(pendingData):
    iTemplateId = pendingData.iTemplateId
    iDataType = pendingData.iDataType
    iProcessId = pendingData.iProcessId
    sfileName = pendingData.sfileName
    sDbDateField = pendingData.sDbDateField
    sSourceDateFormat = pendingData.sSourceDateFormat
    iDestinationDB = pendingData.iDestinationDB
    sDbDateField = pendingData.sDbDateField
    sDbDateCondition = pendingData.sDbDateCondition
    bFileHeaderCheck = pendingData.bFileHeaderCheck

else:
    logger.info('No jobs are pending...\n')
    exit()

qTemplate = mySession.query(tblTemplates).filter(
    tblTemplates.iTemplateId == iTemplateId).first()

qDBConnection = mySession.query(tblDBConnection).filter(
    tblDBConnection.iDBId == iDestinationDB).first()


# MSSQL Connection
msengine = create_engine('mssql+pymssql://{0}:{1}@{2}/{3}'.
                         format(qDBConnection.sUsername, qDBConnection.sPassword,
                                qDBConnection.sHostname, qDBConnection.sDatabasename), pool_pre_ping=True, pool_recycle=3600)
logger.info('Connected to MSSQL DB.')


try:
    qSDBConnection = mySession.query(tblDBConnection).filter(
        tblDBConnection.iDBId == pendingData.iSourceDB).first()
    sUsername = qSDBConnection.sUsername
    sPassword = qSDBConnection.sPassword
    sHostname = qSDBConnection.sHostname
    sDatabasename = qSDBConnection.sDatabasename
    sTablename = qSDBConnection.sTablename
except:
    sUsername = qDBConnection.sUsername
    sPassword = qDBConnection.sPassword
    sHostname = qDBConnection.sHostname
    sDatabasename = qDBConnection.sDatabasename
    sTablename = qDBConnection.sTablename

# Mongo Connection
mng_client = MongoClient('10.10.10.54',
                         username=sUsername,
                         password=sPassword,
                         authSource='admin')
logger.info('Connected to Mongo DB.')
mng_db = mng_client[sDatabasename]
db_cm = mng_db[sTablename]


# File to MSSQL


def fileToMSSQL():

    metadata = MetaData()
    print(qDBConnection.sTablename)
    try:
        mssqlTable = Table(qDBConnection.sTablename, metadata,
                           autoload=True, autoload_with=msengine)
    except:
        logger.info(
            "Connection to MSSQL lost. ERROR(111).")
    sFieldname = qDBConnection.sFieldname.split('||')
    sFieldname = list(filter(None, sFieldname))
    print("before coulmn check")
    for field in sFieldname:
        print(field.split('@@')[0])
        print(mssqlTable.columns.keys())
        print(int(mssqlTable.columns[field.split('@@')[0]].type.length))
        print(int(field.split('@@')[2]))
        if (field.split('@@')[0] not in mssqlTable.columns.keys()) or int(mssqlTable.columns[field.split('@@')[0]].type.length) != int(field.split('@@')[2]) or field.split('@@')[1].upper() not in str(mssqlTable.columns[field.split('@@')[0]].type):
            logger.error("There is a mismatch between given column details and the existing column in table "
                        + qDBConnection.sTablename + ".")
            pendingData.iDataStatus = 4
            pendingData.iTotalCount = df.shape[0]
            mySession.commit()
            exit()
    print("after coulmn check")
    df.to_sql(qDBConnection.sTablename, con=msengine,
              if_exists='append', index=False)
    pendingData.iDataStatus = 3
    pendingData.iTotalCount = df.shape[0]
    mySession.commit()
    logger.info(
        "File's data dumped to MSSQL DB and status changed to Completed.")

# File to Mongo


def fileToMongo():
    df_json = json.loads(df.to_json(orient='records', date_format="iso"))
    db_cm.insert(df_json)
    print(db_cm.count())
    mng_client.close()
    pendingData.iDataStatus = 3
    pendingData.iTotalCount = df.shape[0]
    mySession.commit()
    logger.info(
        "File's data dumped to Mongo DB and status changed to Completed.")

# Mongo to MSSQL


def mongoToMSSQL():
    gte, lte = sDbDateCondition.split(" - ")
    gte = datetime.datetime.strptime(gte, '%d/%m/%Y')
    lte = datetime.datetime.strptime(lte, '%d/%m/%Y')
    if(lte == gte):
        lte += datetime.timedelta(days=1)
    gte.isoformat()
    lte.isoformat()
    # Get Mongo Data
    # Range query : db.php_test.find({date: {$gte:'2018-05-07T00:00:00',$lt: '2018-05-09T00:00:00'}})
    df = pd.DataFrame(
        columns=['date', 'client', 'amount', 'transID', 'serialNumber'])
    cursor = db_cm.find(
        {'date': {'$gte': str(gte), '$lt': str(lte)}}, {'_id': 0})
    df = pd.read_json(dumps(cursor), convert_dates=False)
    formatting(df)
    df.to_sql(qDBConnection.sTablename, con=msengine,
              if_exists='append', index=False)
    mng_client.close()
    pendingData.iDataStatus = 3
    pendingData.iTotalCount = df.shape[0]
    mySession.commit()
    logger.info(
        "Mongo DB's data dumped to MSSQL DB and status changed to Completed.")

# Function to remove special character and set proper date format
def formatting(df):
    # Remove special character
    if df.empty:
        logger.error("There is no data to process.\n")
        pendingData.iDataStatus = 4
        pendingData.iTotalCount = df.shape[0]
        mySession.commit()
        exit()
    logger.info("Formatting Function called.")
    print(df.head())
    regex = re.compile('\'')
    for i in df:
        if(df[i].dtype == object):
            df.loc[:,i] = df.loc[:,i].astype(str)
            df[i] = df[i].map(lambda x: re.sub(regex, '', x))
            df[i] = df[i].apply(lambda x: x.strip())
    logger.info("Special character removed.")
    print(df.head())

    # Date formatting
    # df[sDbDateField] = pd.to_datetime(
    #     df[sDbDateField], format=dateFormat[sSourceDateFormat], errors='ignore')
    print(sDbDateField)
    if(sDbDateField):

        try:
            df.loc[:,sDbDateField] = df.loc[:,sDbDateField].astype(str)
            df[sDbDateField] = df[sDbDateField].map(
                lambda x: datetime.datetime.strptime(str(x), dateFormat[sSourceDateFormat]))
        except:
            logger.error("There is something wrong with date format.\n")
            pendingData.iDataStatus = 4
            pendingData.iTotalCount = df.shape[0]
            mySession.commit()
            exit()
        df[sDbDateField] = df[sDbDateField].map(
            lambda x: datetime.datetime.strftime(x, '%Y-%m-%d %H:%M:%S'))
    logger.info("Date formatting done.")
    print(df.head())
    # exit()
# Dictoinary to hold fuctions
chooseProcess = {1: fileToMongo, 2: fileToMSSQL, 3: mongoToMSSQL}


def runProcess(value):
    chooseProcess.get(value, lambda: 'Invalid')()


sDestinationColumns = qTemplate.sDestinationColumns.split('||')
sDestinationColumns = list(filter(None, sDestinationColumns))

sSourceColumns = qTemplate.sSourceColumns.split('||')
sSourceColumns = list(filter(None, sSourceColumns))
try:
    sSourceColumns = list(map(int, sSourceColumns))
    sSourceColumns = [x - 1 for x in sSourceColumns]
except:
    sSourceColumns = list(map(str, sSourceColumns))
    if(not all(elem in sDestinationColumns for elem in sSourceColumns)):
        logger.info("Destination DB doesn't have Source Column.")
        exit()

srcDstDict = dict(zip(sSourceColumns, sDestinationColumns))


if(sfileName):
    print(sfileName)
    logger.info("Started formatting file " + sfileName + ".")
    file = '/var/www/html/DataProcessor/assets/data/' + sfileName
    files = glob.glob('/var/www/html/DataProcessor/assets/data/*.*')
    # print(files)
    # print(file)
    if file not in files:
        logger.error("File " + sfileName + " doesn't exist to process.\n")
        pendingData.iDataStatus = 4
        pendingData.iTotalCount = df.shape[0]
        mySession.commit()
        exit()

    ext = (".xls", ".xlsx")
    if(file.endswith(ext)):
        # Code for XLS
        with open('dataProcessing.log', 'a') as fp:
            sys.stderr = fp
            df = pd.read_excel(file, warn_bad_lines=True,
                               error_bad_lines=False)
        df = df.iloc[:, sSourceColumns]
        sSourceColumns = list(df.columns)
        srcDstDict = dict(zip(sSourceColumns, sDestinationColumns))
        df.rename(columns=srcDstDict, inplace=True)
        print("Before Regex CSV")
        print(df.head())
    else:
        # Code for CSV
        if bFileHeaderCheck == 1:
            with open('dataProcessing.log', 'a') as fp:
                sys.stderr = fp
                df = pd.read_csv(file, sep=qTemplate.sFileDelimeter, header=0,
                                 engine='python', warn_bad_lines=True, error_bad_lines=False)
            df = df.iloc[:, sSourceColumns]
            sSourceColumns = list(df.columns)
            srcDstDict = dict(zip(sSourceColumns, sDestinationColumns))
            print(df.head())
            df.rename(columns=srcDstDict, inplace=True)
            print("Before Regex CSV")
            print(df.head())

        else:
            with open('dataProcessing.log', 'a') as fp:
                sys.stderr = fp
                df = pd.read_csv(file, sep=qTemplate.sFileDelimeter, header=None,
                                 engine='python', warn_bad_lines=True, error_bad_lines=False)
            # sSourceColumns.sort()
            df = df[sSourceColumns]
            df.rename(columns=srcDstDict, inplace=True)
            print("Before Regex TXT")
            print(df.head())
    # Calling formattnig function defined above
    formatting(df)
    logger.info("Formatting done.")


# Run Specific function defined above
runProcess(iDataType)


# Close Connections
engine.dispose()
msengine.dispose()
logging.info('Process of file ' + sfileName + ' is Completed.\n')
# Number of rows to be processed
# print(df.shape[0])

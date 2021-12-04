import mysql.connector, os, schedule, time
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import re
from pymongo import MongoClient
import json


db_username = 'root'
db_password = 'Passw0rd'
db_ip       = 'localhost'
db_name     = 'DataProcessor'

engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                    format(db_username, db_password,
                                    db_ip, db_name), pool_pre_ping=True, pool_recycle=3600)
Base = automap_base()
Base.prepare(engine, reflect=True)


tblTemplates = Base.classes.tblTemplates
tblDBConnection = Base.classes.tblDBConnection
session = Session(engine)

print()
qTemplate = session.query(tblTemplates).filter(tblTemplates.sTemplateName == "varunxls").first()
qTemplate = dict(qTemplate.__dict__)
# print(qTemplate)
print()
qDBConnection = session.query(tblDBConnection).filter(tblDBConnection.sConnectionName == "varuntest").first()
qDBConnection = dict(qDBConnection.__dict__)
# print(qDBConnection)



sSourceColumns = qTemplate['sSourceColumns'].split('||')
sSourceColumns = list(filter(None, sSourceColumns))
sSourceColumns = list(map(int, sSourceColumns))
sSourceColumns = [x-1 for x in sSourceColumns]


sDestinationColumns = qTemplate['sDestinationColumns'].split('||')
sDestinationColumns = list(filter(None, sDestinationColumns))

sFieldname = qDBConnection['sFieldname'].split('||')
sFieldname = list(filter(None, sFieldname))

srcDstDict = dict(zip(sSourceColumns, sDestinationColumns))

df = pd.read_excel('data/ANDB_DB.xls', )
df = df.iloc[:,sSourceColumns]
sSourceColumns = list(df.columns)
srcDstDict = dict(zip(sSourceColumns, sDestinationColumns))
df.rename(columns=srcDstDict , inplace = True)


regex = re.compile('\'')
for i in df:
    if(df[i].dtype==object):
        df[i] = df[i].map(lambda x: re.sub(regex,'',x))

print(df)


engine.dispose()
qDBConnection['sHostname'] = 'localhost'
engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                    format(qDBConnection['sUsername'], qDBConnection['sPassword'],
                                    qDBConnection['sHostname'], qDBConnection['sDatabasename']), pool_pre_ping=True, pool_recycle=3600)



# print(df.shape[0])
# df['date'] = pd.to_datetime(df['date'].str.strip(), dayfirst=True)
# print(df)

#MySQL
# df.to_sql(qDBConnection['sTablename'], con=engine, if_exists='append', index=False)


# Mongo
mng_client = MongoClient(qDBConnection['sHostname'], 27017)
mng_db = mng_client[qDBConnection['sDatabasename']]
db_cm = mng_db[qDBConnection['sTablename']]
df_json = json.loads(df.to_json(orient='records'))
db_cm.remove()
db_cm.insert(df_json)

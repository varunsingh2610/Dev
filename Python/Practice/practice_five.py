#import mysql.connector, os, schedule, time
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


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
print(qTemplate)
print()
qDBConnection = session.query(tblDBConnection).filter(tblDBConnection.sConnectionName == "varuntest").first()
qDBConnection = dict(qDBConnection.__dict__)
print(qDBConnection)



sSourceColumns = qTemplate['sSourceColumns'].split('||')
sSourceColumns = list(filter(None, sSourceColumns))
sSourceColumns = list(map(int, sSourceColumns))
sSourceColumns = [x-1 for x in sSourceColumns]


sDestinationColumns = qTemplate['sDestinationColumns'].split('||')
sDestinationColumns = list(filter(None, sDestinationColumns))

sFieldname = qDBConnection['sFieldname'].split('||')
sFieldname = list(filter(None, sFieldname))

srcDstDict = dict(zip(sSourceColumns, sDestinationColumns))

# df = pd.read_csv('data/AXIS_NBK.rpt', sep=qTemplate['sFileDelimeter'], header=None,  engine='python', error_bad_lines=False)
df = pd.read_excel('data/ANDB_DB.xls', )
print(df)
# df.drop([0], axis=1, inplace = True)
# df = df.reset_index(drop=True)
# df.rename(columns={"0": "datee","1": "date", "2": "client", "3": "amount", "4": "transID", "5": "serialNumber"}, inplace = True)
# df.rename(columns={ df.columns[0]: "date" }, inplace = True)


# sSourceColumns.sort()
print(sSourceColumns)
df = df.iloc[:,sSourceColumns]

sSourceColumns = list(df.columns)

srcDstDict = dict(zip(sSourceColumns, sDestinationColumns))
df.rename(columns=srcDstDict , inplace = True)
print(sSourceColumns)
print(sDestinationColumns)
print(srcDstDict)
print(df)
# print(df)

engine.dispose()
qDBConnection['sHostname'] = 'localhost'
engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                    format(qDBConnection['sUsername'], qDBConnection['sPassword'],
                                    qDBConnection['sHostname'], qDBConnection['sDatabasename']), pool_pre_ping=True, pool_recycle=3600)




df.to_sql(qDBConnection['sTablename'], con=engine, if_exists='append', index=False)

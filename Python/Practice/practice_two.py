import pymssql
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, create_engine, select)
from sqlalchemy import text
import pandas as pd



db_username = 'avmntr.19818'
db_password = 'M0n1tor$2'
db_name = ''


# [['172.17.6.12\Jridb', 'avmntr.19818' , 'M0n1tor$2' , '' , '12625', 'AVENUES : 172.17.6.12\Jridb'],
####['172.17.6.12\RESEVTDB', 'avmntr.19818' , 'M0n1tor$2' , '' , '12627', 'AVENUES : 172.17.6.12\RESEVTDB'],
# ['172.17.6.17', 'avmntr.19818' , 'M0n1tor$2' , '' , '1433', 'AVENUES : 172.17.6.17'],
# ['172.17.4.24\MCPGMARS', 'avmntr.19818' , 'M0n1tor$2' , '' , '1433', 'AVENUES : 172.17.4.24\MCPGMARS'],
# ['172.17.4.23\MCPGTRANS', 'avmntr.19818' , 'M0n1tor$2' , '' , '12625', 'AVENUES : 172.17.4.23\MCPGTRANS'],
# ['172.17.4.20\PGMARS', 'avmntr.19818' , 'M0n1tor$2' , '' , '1433', 'AVENUES : 172.17.4.20\PGMARS'],
# ['172.17.4.19\PGTRANS', 'avmntr.19818' , 'M0n1tor$2' , '' , '12625', 'AVENUES : 172.17.4.19\PGTRANS'],
# ['172.16.2.15', 'avmntr.19818' , 'M0n1tor$2' , '' , '12625', 'AVENUES : 172.16.2.15'],
# ['172.16.6.4', 'avmntr.19818' , 'M0n1tor$2' , '' , '1433', 'AVENUES : 172.16.6.4'],
# ['172.16.6.6', 'avmntr.19818' , 'M0n1tor$2' , '' , '1433', 'AVENUES : 172.16.6.6'],
# ['172.16.6.2', 'avmntr.19818' , 'M0n1tor$2' , '' , '12625', 'AVENUES : 172.16.6.2']]


SYSPROCESS_QUERY = 'SELECT LTRIM(RTRIM(hostname)) hostname,LTRIM(RTRIM(loginame)) loginame,COUNT(DISTINCT spid) Count,MAX(spid) Max_Session_Id FROM sys.sysprocesses GROUP BY LTRIM(RTRIM(hostname)),LTRIM(RTRIM(loginame)) order by Count desc'

BLOCKLIST_QUERY = 'SELECT percent_complete,session_id,blocking_session_id FROM sys.dm_exec_requests WHERE blocking_session_id <> 0'

CURRENTLIST_QUERY = 'SELECT session_id spid,blocking_session_id blocked_spid,cpu_time,writes,reads,DB_NAME(dbid) db_name,wait_time,wait_type,user_id,DATEDIFF(mi,start_time,GETDATE()) run_time,qt.text FROM sys.dm_exec_requests er CROSS APPLY sys.dm_exec_sql_text(er.sql_handle)as qt WHERE session_id> 50 ORDER BY run_time DESC,cpu_time DESC'

# Connection for MSSQL server

JridbEngine = create_engine('mssql+pymssql://{0}:{1}@{2}:{3}/{4}'.
                         format(db_username, db_password,
                                '172.17.6.12', '12625', db_name), pool_pre_ping=True, pool_recycle=3600)

OneSevenEngine = create_engine('mssql+pymssql://{0}:{1}@{2}:{3}/{4}'.
                         format(db_username, db_password,
                                '172.17.6.17', '1433', db_name), pool_pre_ping=True, pool_recycle=3600)

MCPGMARSEngine = create_engine('mssql+pymssql://{0}:{1}@{2}:{3}/{4}'.
                         format(db_username, db_password,
                                '172.17.4.24', '1433', db_name), pool_pre_ping=True, pool_recycle=3600)

MCPGTRANSEngine = create_engine('mssql+pymssql://{0}:{1}@{2}:{3}/{4}'.
                         format(db_username, db_password,
                                '172.17.4.23', '12625', db_name), pool_pre_ping=True, pool_recycle=3600)

PGMARSEngine = create_engine('mssql+pymssql://{0}:{1}@{2}:{3}/{4}'.
                         format(db_username, db_password,
                                '172.17.4.20', '1433', db_name), pool_pre_ping=True, pool_recycle=3600)

PGTRANSEngine = create_engine('mssql+pymssql://{0}:{1}@{2}:{3}/{4}'.
                         format(db_username, db_password,
                                '172.17.4.19', '12625', db_name), pool_pre_ping=True, pool_recycle=3600)

OneFiveEngine = create_engine('mssql+pymssql://{0}:{1}@{2}:{3}/{4}'.
                         format(db_username, db_password,
                                '172.16.2.15', '12625', db_name), pool_pre_ping=True, pool_recycle=3600)

FourEngine = create_engine('mssql+pymssql://{0}:{1}@{2}:{3}/{4}'.
                         format(db_username, db_password,
                                '172.16.6.4', '1433', db_name), pool_pre_ping=True, pool_recycle=3600)

SixEngine = create_engine('mssql+pymssql://{0}:{1}@{2}:{3}/{4}'.
                         format(db_username, db_password,
                                '172.16.6.6', '1433', db_name), pool_pre_ping=True, pool_recycle=3600)

TwoEngine = create_engine('mssql+pymssql://{0}:{1}@{2}:{3}/{4}'.
                         format(db_username, db_password,
                                '172.16.6.2', '12625', db_name), pool_pre_ping=True, pool_recycle=3600)

JridbDf = pd.read_sql(CURRENTLIST_QUERY, JridbEngine)
print(JridbDf)

JridbDf = pd.read_sql(SYSPROCESS_QUERY, OneSevenEngine)
print(JridbDf)

OneSevenDf = pd.read_sql(SYSPROCESS_QUERY, MCPGMARSEngine)
print(OneSevenDf)

MCPGTRANSDf = pd.read_sql(SYSPROCESS_QUERY, MCPGTRANSEngine)
print(MCPGTRANSDf)

PGMARSDf = pd.read_sql(SYSPROCESS_QUERY, PGMARSEngine)
print(PGMARSDf)

PGTRANSDf = pd.read_sql(SYSPROCESS_QUERY, PGTRANSEngine)
print(PGTRANSDf)

OneFiveDf = pd.read_sql(SYSPROCESS_QUERY, OneFiveEngine)
print(OneFiveDf)

FourDf = pd.read_sql(SYSPROCESS_QUERY, FourEngine)
print(FourDf)

SixDf = pd.read_sql(SYSPROCESS_QUERY, SixEngine)
print(SixDf)

TwoDf = pd.read_sql(SYSPROCESS_QUERY, TwoEngine)
print(TwoDf)

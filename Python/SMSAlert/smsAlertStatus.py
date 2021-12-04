#!/usr/bin/python
#    Created on : 6 Dec, 2018, 11:50:25 AM
#    Author     : Kaushik B. Solanki
#    Edited by  : Varun Singh

import pymssql
from random import randint
from pprint import pprint
from datetime import datetime, timedelta
from collections import defaultdict
import requests
import json

import time
time.sleep(30)


mobileNo = 9930605997
testMobileNo = 8109055354


def logData(filename, now, printdata):
    logger = open("/var/www/Python/SMSAlert/Logs/" + filename + ".log", "a")
    logger.write('\n' + str(datetime.now()) + ' ---> ' + printdata)
    logger.close()


def connectMSSQL(conns):
    months = ["Unknown", "January", "Febuary", "March", "April", "May",
              "June", "July", "August", "September", "October", "November", "December"]

    sysprocessQry = "SELECT LTRIM(RTRIM(hostname)) hostname,LTRIM(RTRIM(loginame)) loginame,COUNT(DISTINCT spid) Count,MAX(spid) Max_Session_Id FROM sys.sysprocesses GROUP BY LTRIM(RTRIM(hostname)),LTRIM(RTRIM(loginame)) order by Count desc"
    blocklistQry = "SELECT percent_complete,session_id,blocking_session_id FROM sys.dm_exec_requests WHERE blocking_session_id <> 0"
    currentlistQry = "SELECT session_id spid,blocking_session_id blocked_spid,cpu_time,writes,reads,DB_NAME(dbid) db_name,wait_time,wait_type,user_id,DATEDIFF(mi,start_time,GETDATE()) run_time,qt.text FROM sys.dm_exec_requests er CROSS APPLY sys.dm_exec_sql_text(er.sql_handle)as qt WHERE session_id> 50 ORDER BY run_time DESC,cpu_time DESC"

    now = (datetime.now())
    year = (now.year)
    month = (months[now.month])
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    filenameSys = "smsAlertSysProcessLogs_" + month + str(year)
    filenameCurr = "smsAlertCurrentProcessLogs_" + month + str(year)
    logData(filenameSys, now, "************************************* SMS ALERTS LOGS FOR " +
            str(now) + " STARTED *************************************")
    logData(filenameCurr, now, "************************************* SMS ALERTS LOGS FOR " +
            str(now) + " STARTED *************************************")
    listData = defaultdict(list)

    for i in range(len(conns)):
        server = conns[i][0]
        user = conns[i][1]
        password = conns[i][2]
        port = conns[i][4]
        # print(port)
        logData(filenameSys, now, "Establishing connection to MSSQL Server " +
                server + " Started.......")
        logData(filenameCurr, now, "Establishing connection to MSSQL Server " +
                server + " Started.......")
        try:
            # print("in try")
            conn = pymssql.connect(
                server=server, user=user, password=password, database='', port=port)
            logData(filenameSys, now, "MSSQL Connection Succeeded .......")
            logData(filenameCurr, now, "MSSQL Connection Succeeded .......")
            cursor = conn.cursor(as_dict=True)

            ################################## Sysprocess #######################################
            cntSysWarn = 0
            cntSysAlert = 0
            logData(filenameSys, now,
                    "<-- Processing Query for Sysprocess Started-->")
            cursor.execute(sysprocessQry)
            sysprocesses = cursor.fetchall()
            for key, val in enumerate(sysprocesses):
                # print(server)
                # print(key, val)
                count = val['Count']
                if server == "172.17.6.12\Jridb":
                    if count > 200 and count < 251:
                        logData(filenameSys, now, "Warning -->  Count : " + str(count) + " , Max Session Id : " + str(
                            val['Max_Session_Id']) + " , Hostname : " + str(val['hostname']) + " , Loginame : " + str(val['loginame']))
                        cntSysWarn += 1
                    elif count > 250:
                        logData(filenameSys, now, "Error -->  Count : " + str(count) + " , Max Session Id : " + str(
                            val['Max_Session_Id']) + " , Hostname : " + str(val['hostname']) + " , Loginame : " + str(val['loginame']))
                        cntSysAlert += 1
                else:
                    if count > 180 and count < 201:
                        logData(filenameSys, now, "Warning -->  Count : " + str(count) + " , Max Session Id : " + str(
                            val['Max_Session_Id']) + " , Hostname : " + str(val['hostname']) + " , Loginame : " + str(val['loginame']))
                        cntSysWarn += 1
                    elif count > 250:
                        logData(filenameSys, now, "Error -->  Count : " + str(count) + " , Max Session Id : " + str(
                            val['Max_Session_Id']) + " , Hostname : " + str(val['hostname']) + " , Loginame : " + str(val['loginame']))
                        cntSysAlert += 1
            logData(filenameSys, now,
                    "<-- Processing Query for Sysprocess Completed-->")
            listData[server].append(cntSysWarn)
            listData[server].append(cntSysAlert)
            listData[server].append(val['Count'])
            ################################## Sysprocess #######################################

            ################################## Blocklist #######################################
            '''cntBlockWarn = 0
            logData(filename,now,"<-- Processing Query for BlockList Started-->")
            cursor.execute(blocklistQry)
            blocklist = cursor.fetchall()
            cntblocklist = len(blocklist)
            if cntblocklist > 0 :
               for key,val in enumerate(blocklist):
                   logData(filename,now,"Warning -->  % COMPLETE : "+ str(val['percent_complete']) +" , SESSION ID : "+ str(val['session_id'])+" , BLOCKING SESSION ID : "+ str(val['blocking_session_id']))
                   cntBlockWarn += 1
            logData(filename,now,"<-- Processing Query for BlockList End-->")
            listData[server].append(cntBlockWarn)'''
            ################################## BlockList  #######################################

            ################################## Current #######################################
            cntCurrWarn = 0
            cntCurrAlert = 0
            logData(filenameCurr, now,
                    "<-- Processing Query for Currentprocess Started-->")
            cursor.execute(currentlistQry)
            currentlist = cursor.fetchall()
            for key, val in enumerate(currentlist):
                runtime = val['run_time']
                if runtime > 10 and runtime < 16:
                    logData(filenameCurr, now, "Warning -->  Session Id : " + str(val['spid']) + " , Blocked Session Id : " + str(val['blocked_spid']) + " , CPU Time : " + str(val['cpu_time']) + " , Writes : " + str(val['writes']) + " , Reads : " + str(
                        val['reads']) + " , DB NAME : " + str(val['db_name']) + " , Wait Time : " + str(val['wait_time']) + " , Wait Type : " + str(val['wait_type']) + " , User Id : " + str(val['user_id']) + ", Run Time : " + str(val['run_time']) + " , Text : " + str(val['text']))
                    cntCurrWarn += 1
                elif runtime > 15:
                    logData(filenameCurr, now, "Error -->  Session Id : " + str(val['spid']) + " , Blocked Session Id : " + str(val['blocked_spid']) + " , CPU Time : " + str(val['cpu_time']) + " , Writes : " + str(val['writes']) + " , Reads : " + str(
                        val['reads']) + " , DB NAME : " + str(val['db_name']) + " , Wait Time : " + str(val['wait_time']) + " , Wait Type : " + str(val['wait_type']) + " , User Id : " + str(val['user_id']) + ", Run Time : " + str(val['run_time']) + " , Text : " + str(val['text']))
                    cntCurrAlert += 1
            logData(filenameCurr, now,
                    "<-- Processing Query for Currentprocess Completed-->")
            listData[server].append(cntCurrWarn)
            listData[server].append(cntCurrAlert)
            ################################## Current #######################################
            # print("connection close")
            conn.close()

        except:

            # print(server)
            URL = "http://sms6.rmlconnect.net/bulksms/bulksms?"
            destination = mobileNo
            message = "Connection Error\n\nServer : " + \
                server + "\n\nNot able to connect to this server"
            PARAMS = {'username': "avenues", "password": "zerb5rv", "type": "0",
                      "dlr": "1", "destination": destination, "source": "CCAVEN", "message": message}
            response = requests.get(url=URL, params=PARAMS)
            logData(filenameSys, now,
                    "Failed connection to MSSQL Server " + server + ".......")
            logData(filenameCurr, now,
                    "Failed connection to MSSQL Server " + server + ".......")

        logData(filenameSys, now,
                "Establishing connection to MSSQL Server " + server + " End.......")
        logData(filenameCurr, now,
                "Establishing connection to MSSQL Server " + server + " End.......")

    msg = "Alerts & Warnings --> \n"
    cntmsg = 0
    # print(listData)
    for key, val in enumerate(listData):
        # print(listData)
        Sysprocess = listData[val][0] + listData[val][1]
        #Blocklist = listData[val][2]
        Currentprocess = listData[val][2] + listData[val][3]
        # if Sysprocess > 0 or Currentprocess > 2:
        if Sysprocess > 0:
            msg += val + " :\n"
            if Sysprocess > 0:
                msg += "(Session Count - " + str(Sysprocess) + ")\n"
                cntmsg += 1

            '''if Currentprocess > 2:
               msg += "(Session List - "+ str(Currentprocess) +")\n"
               cntmsg += 1'''
    # print(cntmsg)
    if cntmsg > 0:
        # OLD URL = "https://sms6.routesms.com/bulksms/bulksms?"
        URL = "http://sms6.rmlconnect.net/bulksms/bulksms?"
        destination = mobileNo
        PARAMS = {'username': "avenues", "password": "zerb5rv", "type": "0",
                  "dlr": "1", "destination": destination, "source": "CCAVEN", "message": msg}
        response = requests.get(url=URL, params=PARAMS)
        logData(filenameSys, now, "SMS Request :" + str(PARAMS))
        logData(filenameCurr, now, "SMS Request :" + str(PARAMS))
        logData(filenameSys, now, "SMS Response :" + str(response))
        logData(filenameCurr, now, "SMS Response :" + str(response))
    else:
        # OLD URL = "https://sms6.routesms.com/bulksms/bulksms?"
        URL = "http://sms6.rmlconnect.net/bulksms/bulksms?"
        destination = testMobileNo
        PARAMS = {'username': "avenues", "password": "zerb5rv", "type": "0",
                  "dlr": "1", "destination": destination, "source": "CCAVEN", "message": msg}
        # response = requests.get(url=URL, params=PARAMS)
        logData(filenameSys, now, "No Alerts and Warnings Found on any Servers")
        logData(filenameCurr, now, "No Alerts and Warnings Found on any Servers")

    logData(filenameSys, now, "************************************* SMS ALERTS LOGS FOR " +
            str(now) + " ENDED *************************************")
    logData(filenameCurr, now, "************************************* SMS ALERTS LOGS FOR " +
            str(now) + " ENDED *************************************")
    exit(1)


conns = [
        ['172.17.4.24\MCPGMARS', 'avmntr.19818', 'M0n1tor$2', '', '1433', 'AVENUES : 172.17.4.24\MCPGMARS'],
    ['172.17.4.23\MCPGTRANS', 'avmntr.19818', 'M0n1tor$2', '', '12625', 'AVENUES : 172.17.4.23\MCPGTRANS'],
    ['172.17.6.12\Jridb', 'avmntr.19818', 'M0n1tor$2', '', '12625', 'AVENUES : 172.17.6.12\Jridb']
]


otherConns = [['172.17.6.17', 'avmntr.19818', 'M0n1tor$2', '', '1433', 'AVENUES : 172.17.6.17'],
              ['172.17.4.20\PGMARS', 'avmntr.19818', 'M0n1tor$2', '', '1433', 'AVENUES : 172.17.4.20\PGMARS'],
              ['172.17.4.19\PGTRANS', 'avmntr.19818', 'M0n1tor$2', '', '12625', 'AVENUES : 172.17.4.19\PGTRANS'],
              ['172.17.4.42', 'avmntr.19818', 'M0n1tor$2', '', '12626', 'AVENUES : 172.17.4.42\AEMARS'],
              ['172.17.4.43', 'avmntr.19818', 'M0n1tor$2', '', '12625', 'AVENUES : 172.17.4.43\AETRANS'],
              # ['172.16.2.15', 'avmntr.19818' , 'M0n1tor$2' , '' , '12625', 'AVENUES : 172.16.2.15'],
              # ['172.16.6.4', 'avmntr.19818' , 'M0n1tor$2' , '' , '1433', 'AVENUES : 172.16.6.4'],
              # ['172.16.6.6', 'avmntr.19818' , 'M0n1tor$2' , '' , '1433', 'AVENUES : 172.16.6.6'],
              # ['172.16.6.2', 'avmntr.19818' , 'M0n1tor$2' , '' , '12625', 'AVENUES : 172.16.6.2']
              ]

# print("before connconnectMSSQL")

for i in range(len(otherConns)):

    # logData(filenameSys, now, "Establishing connection to MSSQL Server " +
    #         server + " Started.......")
    # logData(filenameCurr, now, "Establishing connection to MSSQL Server " +
    #         server + " Started.......")
    try:
        connection = pymssql.connect(
            server=otherConns[i][0], user=otherConns[i][1], password=otherConns[i][2], database='', port=otherConns[i][4])
        # logData(filenameSys, now, "MSSQL Connection Succeeded .......")
        # logData(filenameCurr, now, "MSSQL Connection Succeeded .......")
        cursor = connection.cursor(as_dict=True)
        # print("connection success!")
    except:
        # print(server)
        URL = "http://sms6.rmlconnect.net/bulksms/bulksms?"
        # destination = mobileNo
        destination = testMobileNo
        message = "Connection Error\n\nServer : " + \
            otherConns[i][5] + "\n\nNot able to connect to this server"
        PARAMS = {'username': "avenues", "password": "zerb5rv", "type": "0",
                  "dlr": "1", "destination": destination, "source": "CCAVEN", "message": message}
        response = requests.get(url=URL, params=PARAMS)
    print("working ok!")


connectMSSQL(conns)
# print("after connconnectMSSQL")

import mysql.connector, os, sqlalchemy, schedule, time
import pandas as pd



database_username = 'root'
database_password = 'Passw0rd'
database_ip       = '127.0.0.1'
database_name     = 'python'
engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                    format(database_username, database_password,
                                    database_ip, database_name), pool_recycle=3600)

path = '/home/varun.singh/Dev/Python/Practice/data'
ext = (".xls", ".xlsx")

def job():
    df.to_sql(con=engine, name='tableTest', if_exists='replace')


for filename in os.listdir(path):
    if(filename.endswith(ext)):
        df = pd.read_excel('data/'+filename, header=0)
        print(filename)
        print(df)

    else:
        df = pd.read_csv('data/'+filename, sep="\^|\||\~|\,", header=None,  engine='python', error_bad_lines=False)
        print(filename)
        print(df)


    # schedule.every(.5).minutes.do(job)
    schedule.every(5).seconds.do(job)

    while 1:
        schedule.run_pending()
        time.sleep(1)


# df = pd.read_csv('data/ALBD_NBK.txt', sep="\^|\||\~|\,", header=None,  engine='python', error_bad_lines=False)
# print(df)
# df.to_sql(con=engine, name='tableTest', if_exists='replace')

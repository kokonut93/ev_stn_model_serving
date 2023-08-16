from private import db_info
import pandas as pd
import numpy as np
import datetime
import pymysql
import torch

# get current datetime
def get_dt():
    now = datetime.datetime.now()
    dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute//20*20, 00)
    str_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt, str_dt

# get realtime datetime
def get_rdt(n):
    dt_realtime = []
    dt, _ = get_dt()
    for i in range(n-1, -1, -1):
        if i == 0 or i == n-1:
            rdt = dt - datetime.timedelta(minutes = 20*(i+1))
            rdt = datetime.datetime(rdt.year-1, rdt.month-6,rdt.day, rdt.hour, rdt.minute, 00)
            dt_realtime.append(rdt.strftime('%Y-%m-%d %H:%M:%S'))
    return dt_realtime

# get historical datetime
def get_hdt(n):
    dt_historical = []
    dt, _ = get_dt()
    for i in range(n):
        hdt = dt - datetime.timedelta(days = 7*(i+1))
        hdt = datetime.datetime(hdt.year-1, hdt.month-6, hdt.day, hdt.hour, hdt.minute, 00)
        dt_historical.append(hdt.strftime('%Y-%m-%d %H:%M:%S'))
    return dt_historical

# connect to database by pymysql
def db_connect():
    host, user, password, db = db_info()

    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        charset='utf8',
        port = 3306
    )

    return connection

# get realtime sequence inputs from database
def db2Rseq():
    connection = db_connect()
    start, end = get_rdt(12)
    select_query = f"SELECT * FROM sequence WHERE Time BETWEEN '{start}' AND '{end}'"

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchall()
        connection.close()

    df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])
    return torch.tensor(df.set_index('Time').T.values.reshape(len(cursor.description)-1, -1, 1))

# get historical sequence inputs from database
def db2Hseq():
    connection = db_connect()
    values = tuple(get_hdt(4))
    select_query = f'SELECT * FROM sequence WHERE Time IN {values}'

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchall()
        connection.close()

    df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])
    return torch.tensor(df.set_index('Time').T.values.reshape(len(cursor.description)-1, -1, 1))

# get time index
def dt2T():
    connection = db_connect()
    select_query = "SELECT * FROM sequence LIMIT 1"
    with connection.cursor() as cursor:
        cursor.execute(select_query)
        _ = cursor.fetchall()
        connection.close()

    dt, _ = get_dt()
    time_idx = dt.hour * 3 + dt.minute // 20
    weekday = dt.weekday()
    dow = weekday//5
    T = np.array([time_idx, weekday, dow]).reshape(1, -1)
    T = np.repeat(T, repeats = len(cursor.description)-1, axis = 0)
    return torch.tensor(T)

# get station inputs from database
def db2S():
    connection = db_connect()
    select_query = "SELECT * FROM station"

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchall()
        connection.close()

    df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])
    attr_cols = ['Sid', 'Latitude', 'Longitude', 'Capacity', 'Slow_Chargers',
                 'Fast_Chargers', 'Mean_trip', 'Length_city', 'Length_highway',
                 'Length_local', 'Length_national', 'Indust_ratio', 'Etc_ratio',
                 'Green_ratio', 'Commerce_ratio', 'Reside_ratio']

    embed_cols = ['Sid', 'UMAP_1', 'UMAP_2', 'UMAP_3', 'UMAP_4', 
                  'UMAP_5', 'UMAP_6', 'UMAP_7', 'UMAP_8']

    attrs = torch.tensor(df.loc[:, attr_cols].values)
    embed = torch.tensor(df.loc[:, embed_cols].values)

    return attrs, embed

# update outputs data to database
def y2db(outputs):
    connection = db_connect()

    select_query = "SELECT sid FROM station"

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchall()
    
    update_query = "UPDATE occupancy SET Occupancy_20 = %s, Occupancy_60 = %s, Occupancy_120 = %s WHERE Sid = %s"
    for sid in result:
        values = tuple(outputs[sid[0]] + list(sid))
        with connection.cursor() as cursor:
            cursor.execute(update_query, values)
        
    connection.commit()
    connection.close()
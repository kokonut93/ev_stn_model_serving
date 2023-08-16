from datetime import datetime
import pandas as pd
import pymysql
import json
import torch
from test.private import db_info

def get_dt():
    now = datetime.datetime.now()
    dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute//20*20, 00)
    str_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt, str_dt

def get_in_dt(n):
    in_dt = []
    dt, _ = get_dt()
    for i in range(n):
        if i == 0 or i == n-1:
            idt = dt - datetime.timedelta(minutes = 20*(i+1))
            in_dt.append(idt.strftime('%Y-%m-%d %H:%M:%S'))
    return in_dt

def get_out_dt(n):
    out_dt = []
    dt, _ = get_dt()
    for i in range(n):
        if i == 0 or i == n-1:
            odt = dt + datetime.timedelta(minutes = 20*(i+1))
            out_dt.append(odt.strftime('%Y-%m-%d %H:%M:%S'))
    return out_dt

def json2tensor(json_data):
    X = []
    sids = list(json_data.keys())
    for sid in sids:
        X.append(list(json_data[sid].values()))

    return sids, torch.tensor(X)

def tensor2json(sids, outputs):
    dict = {}
    for idx in range(len(outputs)):
        dict[sids[idx]] = int(outputs[idx].argmax())
    
    return json.dumps(dict)

def selectXjson(time):
    host, user, password, db = db_info()

    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        charset='utf8',
        port = 3306
    )

    select_query = "SELECT * FROM station"

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchall()

    df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])
    atts_cols = ['Latitude', 'Longitude', 'Capacity', 'Slow_Chargers',
        'Fast_Chargers', 'Mean_trip', 'Length_city', 'Length_highway',
        'Length_local', 'Length_national', 'Indust_ratio', 'Etc_ratio',
        'Green_ratio', 'Commerce_ratio', 'Reside_ratio']

    embed_cols = ['UMAP_1', 'UMAP_2', 'UMAP_3', 
            'UMAP_4', 'UMAP_5', 'UMAP_6', 'UMAP_7', 'UMAP_8']

    atts = df.loc[:, atts_cols].to_dict('index')
    embed = df.loc[:, embed_cols].to_dict('index')

    select_query = f"SELECT * FROM sequence WHERE Datetime = {time}"

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchall()

    df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])

    return atts, embed, df

def updateYjson(y_json):
    host, user, password, db = db_info()

    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        charset='utf8',
        port = 3306
    )

    create_query = '''
CREATE TABLE occupancy (
Sid INT NOT NULL PRIMARY KEY, 
Occupancy_20 INT NOT NULL,
Occupancy_60 INT NOT NULL,
Occupancy_120 INT NOT NULL,
FOREIGN KEY (sid) REFERENCES station(sid)
)
'''
    select_query = "SELECT sid FROM station"

    insert_query = "INSERT INTO station VALUES {};"

    update_query = "UPDATE occupancy SET Occupancy_20 = %d Occupancy_60 = %d Occupancy_120 = %d WHERE Sid = %d"

    try:
        with connection.cursor() as cursor:
                cursor.execute(create_query.replace('\n', ''))
                cursor.execute(select_query)
                result = cursor.fetchall()

        insert_query = "INSERT INTO occupancy VALUES {};"
        for idx in result:
            values = tuple(list(idx) + y_json[idx[0]])
            with connection.cursor() as cursor:
                cursor.execute(insert_query.format(values))
            
        connection.commit()
        connection.close()
    
    except:
        with connection.cursor() as cursor:
            cursor.execute(select_query)
            result = cursor.fetchall()
        
        update_query = "UPDATE occupancy SET Occupancy_20 = %s, Occupancy_60 = %s, Occupancy_120 = %s WHERE Sid = %s"
        for idx in result:
            values = tuple(y_json[idx[0]] + list(idx))
            with connection.cursor() as cursor:
                cursor.execute(update_query, values)
            
        connection.commit()
        connection.close()
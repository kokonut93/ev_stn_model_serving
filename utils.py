from datetime import datetime
import pandas as pd
import pymysql
import json
import torch
from private import db_info

def get_dt():
    now = datetime.now()
    dt = datetime(now.year, now.month, now.day, now.hour, now.minute//20*20, 00)
    dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt

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



def getXjson():
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
    return atts, embed

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
        with connection.curosr() as cursor:
            cursor.execute(update_query, tuple(y_json[idx[0]], list(idx)))
            connection.commit()
            connection.close()
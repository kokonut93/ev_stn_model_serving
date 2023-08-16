# Create Station's Table
import pandas as pd
from utils import db_connect

# Create Station's Table
def create_station(attrs, embed):
    connection = db_connect()
    create_query = '''
CREATE TABLE IF NOT EXISTS station (
Sid INT NOT NULL PRIMARY KEY, 
Sname VARCHAR(100) NOT NULL, 
Latitude DOUBLE NOT NULL, 
Longitude DOUBLE NOT NULL, 
Capacity FLOAT NOT NULL, 
Slow_Chargers INT NOT NULL,
Fast_Chargers INT NOT NULL,
Mean_trip DOUBLE NOT NULL,
Length_city DOUBLE NOT NULL,
Length_highway DOUBLE NOT NULL,
Length_local DOUBLE NOT NULL,
Length_national DOUBLE NOT NULL,
Indust_ratio DOUBLE NOT NULL,
Etc_ratio DOUBLE NOT NULL,
Green_ratio DOUBLE NOT NULL,
Commerce_ratio DOUBLE NOT NULL,
Reside_ratio DOUBLE NOT NULL,
UMAP_1 DOUBLE NOT NULL,
UMAP_2 DOUBLE NOT NULL,
UMAP_3 DOUBLE NOT NULL,
UMAP_4 DOUBLE NOT NULL,
UMAP_5 DOUBLE NOT NULL,
UMAP_6 DOUBLE NOT NULL,
UMAP_7 DOUBLE NOT NULL,
UMAP_8 DOUBLE NOT NULL
)
'''

    with connection.cursor() as cursor:
        cursor.execute(create_query.replace('\n', ''))

    for idx in range(attrs.shape[0]):
        attr = attrs.iloc[idx, :].values.tolist()
        emb = embed.iloc[idx, :].values.tolist()
        values = tuple(attr + emb[2:])
        insert_query = "INSERT INTO station VALUES {};"
        
        with connection.cursor() as cursor:
            cursor.execute(insert_query.format(values))

    connection.commit()
    connection.close()



# Create Sequence's Table
def create_sequence(seq):
    connection = db_connect()
    
    create_query = "CREATE TABLE IF NOT EXISTS sequence ({} PRIMARY KEY (Time))"
    cols = ''.join(['Time DATETIME NOT NULL, '] + [f'Sid_{col} INT NOT NULL, ' for col in seq.columns[1:]])

    with connection.cursor() as cursor:
        cursor.execute(create_query.format(cols))

    for _, row in seq.iterrows():
        values = tuple(row.values.tolist())

        insert_query = "INSERT INTO sequence VALUES {};".format(values)
        
        with connection.cursor() as cursor:
            cursor.execute(insert_query.format(values))

    connection.commit()
    connection.close()


# Create Occupancy's Table
def create_occupancy():
    connection = db_connect()
    create_query = '''
CREATE TABLE occupancy (
Sid INT NOT NULL PRIMARY KEY, 
Occupancy_20 INT NOT NULL,
Occupancy_40 INT NOT NULL,
Occupancy_60 INT NOT NULL,
Occupancy_80 INT NOT NULL,
Occupancy_100 INT NOT NULL,
Occupancy_120 INT NOT NULL,
FOREIGN KEY (sid) REFERENCES station(sid)
)
'''

    select_query = "SELECT sid FROM station"


    with connection.cursor() as cursor:
        cursor.execute(create_query.replace('\n', ''))
        cursor.execute(select_query)
        result = cursor.fetchall()

        insert_query = "INSERT INTO occupancy VALUES {};"
        for idx in result:
            values = tuple(list(idx) + [0, 0, 0, 0, 0, 0])
            with connection.cursor() as cursor:
                cursor.execute(insert_query.format(values))
            
    connection.commit()
    connection.close()


def __main__():
    attrs = pd.read_csv('data/station_attrs.csv')
    embed = pd.read_csv('data/station_embed.csv')
    seq = pd.read_csv('data/station_seq.csv')

    create_station(attrs, embed)
    create_sequence(seq)
    create_occupancy()
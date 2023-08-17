# Create Station's Table
import pandas as pd
from utils import db_connect

# Create Station's Table
def create_station(attrs, embed):
    connection = db_connect()
    create_query = "CREATE TABLE IF NOT EXISTS station ({}PRIMARY KEY (Sid))"
    cols = attrs.columns.tolist()[2:] + embed.columns.tolist()[2:]
    values = ''.join(['Sid INT NOT NULL, ' 'Sname VARCHAR(100) NOT NULL, '] + [f'{col} DOUBLE NOT NULL, ' for col in cols])

    with connection.cursor() as cursor:
        cursor.execute(create_query.format(values))

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
    
    create_query = "CREATE TABLE IF NOT EXISTS sequence ({}PRIMARY KEY (Time))"
    values = ''.join(['Time DATETIME NOT NULL, '] + [f'Sid_{col} INT NOT NULL, ' for col in seq.columns[1:]])

    with connection.cursor() as cursor:
        cursor.execute(create_query.format(values))

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
    create_query = "CREATE TABLE IF NOT EXISTS occupancy ({}FOREIGN KEY (Sid) REFERENCES station(Sid))"
    values = ''.join(['Sid INT NOT NULL PRIMARY KEY, '] + [f'Occupancy_{i} INT NOT NULL, ' for i in range(20, 121, 20)])

    select_query = "SELECT sid FROM station"


    with connection.cursor() as cursor:
        cursor.execute(create_query.format(values))
        cursor.execute(select_query)
        result = cursor.fetchall()

        insert_query = "INSERT INTO occupancy VALUES {};"
        for idx in result:
            values = tuple(list(idx) + [0, 0, 0, 0, 0, 0])
            with connection.cursor() as cursor:
                cursor.execute(insert_query.format(values))
            
    connection.commit()
    connection.close()


if __name__=="__main__":
    attrs = pd.read_csv('data/station_attrs.csv')
    embed = pd.read_csv('data/station_embed.csv')
    seq = pd.read_csv('data/station_seq.csv')

    create_station(attrs, embed)
    create_sequence(seq)
    create_occupancy()
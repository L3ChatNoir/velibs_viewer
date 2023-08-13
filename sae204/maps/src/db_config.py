import pandas as pd
import mysql.connector as sqlink
from datetime import datetime
import json
import time

def urljson_to_df(url : str) -> pd.DataFrame:
    '''
        Take a url string who have data with JSON format and return a Dataframe of this data

        >>> urljson_to_df('https:url.json')
    '''
    try:
        return pd.read_json(url)
    except Exception as e:
        print('Error, bad url/bad data, Must be JSON File.', e)

def clean_df(df : pd.DataFrame) -> pd.DataFrame:
    '''
        Take a Dataframe and return him with new colums date (date now) and selected colums:
            'stationcode', 'is_installed', 'numdocksavailable', 'numbikesavailable', 'mechanical', 'ebike', 'nom_arrondissement_communes'

        >>> clean_df(urljson_to_df('https:url.json'))
    '''
    date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S" )
    df = df[['stationcode', 'is_installed', 'numdocksavailable', 'numbikesavailable', 'mechanical', 'ebike', 'nom_arrondissement_communes']]
    df.insert(loc = 0, column='date' ,value = [date for i in range(len(df.index))])
    return df

def conect_mysql() -> sqlink:
    '''
        Return mysql connection at root on localhost for database velibs
    '''
    return sqlink.connect(host = 'localhost', user = 'root', password = '', database = 'velibs')

def create_table_mysql():
    '''
        Create tables on mysql : 
            - station_information
            - station_status
            - history_change

        WARNING If tables already exist, they are drop first and next create
    '''

    #Pour chaque tables, si elle existe déjà, on drop la table puis on la crée
    conect = conect_mysql()
    db = conect.cursor()
    db.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'station_information' ")
    if db.fetchone()[0] == 1:
        db.execute('DROP TABLE station_information')
    db.execute('CREATE TABLE station_information (stationcode VARCHAR(100) PRIMARY KEY, name VARCHAR(100), capacity INTEGER, coordonnees_geo VARCHAR(100))')
    
    db.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'station_status' ")
    if db.fetchone()[0] == 1:
        db.execute('DROP TABLE station_status')
    db.execute('CREATE TABLE station_status (date DATETIME, stationcode VARCHAR(100), is_installed VARCHAR(100), numdocksavailable INTEGER, numbikesavailable INTEGER, mechanical INTEGER, ebike INTEGER, nom_arrondissement_communes VARCHAR(100), PRIMARY KEY (date, stationcode))')

    db.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'history_change' ")
    if db.fetchone()[0] == 1:
        db.execute('DROP TABLE history_change')
    db.execute('CREATE TABLE history_change (date_time DATETIME, table_use VARCHAR(50), action VARCHAR(50), stationcode VARCHAR(100), user VARCHAR(50))')

    #Création des trigger sur les tables station_information, station_status à partir du fichier texte trigger.txt (NON UTILSER)
    #with open('trigger.txt', 'r') as file:
    #    sqlfile = file.read()
    #    sqlcommands = sqlfile.split(';')

    #for command in sqlcommands:
    #    db.execute(command)
    #    conect.commit()

    #Création des trigger sur les tables station_information, station_status
    for table in ('status', 'information'):
        for action in ('INSERT', 'UPDATE'):
            db.execute(f'DROP TRIGGER IF EXISTS logs_{action.lower()}_{table};')
            conect.commit()
            db.execute(f"CREATE TRIGGER logs_{action}_{table} AFTER {action} ON station_{table} FOR EACH ROW " +
                        f"INSERT INTO history_change (date_time, table_use, action, stationcode, user) "+
                        f"VALUES (NOW(), 'station_{table}', '{action}', new.stationcode, CURRENT_USER);")
            conect.commit()
        db.execute(f"CREATE TRIGGER logs_delete_{table} AFTER DELETE ON station_{table} FOR EACH ROW " +
                        f"INSERT INTO history_change (date_time, table_use, action, stationcode, user) "+
                        f"VALUES (NOW(), 'station_{table}', 'DELETE', old.stationcode, CURRENT_USER);")
        conect.commit()
        
def insert_table_status(df : pd.DataFrame):
    '''
        Take a DataFrame and insert into mysql table station_status data of this DataFrame

        >>> insert_table_status(clean_df(urljson_to_df('https:url.json')))
    '''
    sql = 'INSERT INTO station_status (date, stationcode, is_installed, numdocksavailable, numbikesavailable, mechanical, ebike, nom_arrondissement_communes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    conect = conect_mysql()
    db = conect.cursor()
    for i in df.index:
        db.execute(sql, (df['date'][i], str(df['stationcode'][i]), df['is_installed'][i], int(df['numdocksavailable'][i]), int(df['numbikesavailable'][i]), int(df['mechanical'][i]), int(df['ebike'][i]), df['nom_arrondissement_communes'][i]))
    conect.commit()

def insert_table_information(df : pd.DataFrame):
    '''
        Take a DataFrame and insert into mysql table station_information data of this DataFrame

        >>> insert_table_information(clean_df(urljson_to_df('https:url.json')))
    '''
    sql = 'INSERT INTO station_information (stationcode, name, capacity, coordonnees_geo) VALUES (%s,%s,%s,%s)'
    conect = conect_mysql()
    db = conect.cursor()
    for i in df.index:
        db.execute(sql, (str(df['stationcode'][i]), df['name'][i], int(df['capacity'][i]), json.dumps(df['coordonnees_geo'][i])))
    conect.commit()

def update_table_status(delta: int, url: str):
    '''
        Take a delta in seconds, a url in str. Every delta seconds insert into my sql table station_status data from url.

        Data from url MUST BE on JSON Format

        >>> update_table_status(60, 'https:url.json')
    '''
    while True:
        try:
            insert_table_status(clean_df(urljson_to_df(url)))
            print(f'Insertion table status effectuer à {datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S" )}')
        except Exception as e:
            print(e)
            pass
        time.sleep(delta)

if __name__ == '__main__':
    # addresse de téléchargement au format JSON
    url1 = 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json?lang=fr&timezone=Europe%2FBerlin'
    url2 = 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-emplacement-des-stations/exports/json?lang=fr&timezone=Europe%2FBerlin'

    # affichage réduit du contenu du fichier CSV
    df_status= clean_df(urljson_to_df(url1))
    df_information= urljson_to_df(url2)
    #print(urljson_to_df(url2))
    insert_table_status(df_status)
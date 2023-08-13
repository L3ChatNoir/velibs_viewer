from .db_config import *
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt
import pandas as pd

def take_data(colums : str ,table : str) -> pd.DataFrame:
    '''
    Return a Dataframe contain data of colums from table from velibs DataBase 
    '''

    df = pd.read_sql(f"SELECT {colums} FROM {table}", con=conect_mysql())
    return df

def take_data_station(colums : str ,table : str, stationcode: str) -> pd.DataFrame:
    '''
    Return a Dataframe contain data of colums from table from velibs DataBase 
    '''

    df = pd.read_sql(f"SELECT {colums} FROM {table} WHERE stationcode = {stationcode}", con=conect_mysql())
    return df

def take_data_date(colums : str ,table : str ,datemin : str , datemax : str) -> pd.DataFrame:
    '''
    Return a Dataframe contain data of colums from table from velibs DataBase Between datemin and datemax
    '''

    datemin = datetime.strptime(datemin, "%Y-%m-%d %H:%M:%S" )
    datemax = datetime.strptime(datemax, "%Y-%m-%d %H:%M:%S" )
    df = pd.read_sql(f"SELECT {colums} FROM {table} WHERE date BETWEEN '{datemin}' AND '{datemax}'", con=conect_mysql())
    return df

def take_data_lastestdate(colums : str ,table : str) -> pd.DataFrame:
    '''
    Return a Dataframe contain data of colums from table from velibs DataBase oder by desc
    '''
    
    df = pd.read_sql(f"SELECT {colums} FROM {table} ORDER BY date DESC", con=conect_mysql())
    return df

def take_data_date_district(colums : str ,table : str ,datemin : str , datemax : str, district : str) -> pd.DataFrame:
    '''
    Return a Dataframe contain data of colums from table from velibs DataBase for a special district
    '''

    df = pd.read_sql(f"SELECT {colums} FROM {table} WHERE nom_arrondissement_communes LIKE '{district}' AND date BETWEEN '{datemin}' AND '{datemax}'", con=conect_mysql())
    return df
    
def take_data_date_station(colums : str ,table : str ,datemin : str , datemax : str, stationcode : str) -> pd.DataFrame:
    '''
    Return a Dataframe contain data of colums from table from velibs DataBase Between datemin and datemax for specifical station
    '''

    datemin = datetime.strptime(datemin, "%Y-%m-%d %H:%M:%S" )
    datemax = datetime.strptime(datemax, "%Y-%m-%d %H:%M:%S" )
    df = pd.read_sql(f"SELECT {colums} FROM {table} WHERE stationcode = {stationcode} AND date BETWEEN '{datemin}' AND '{datemax}'", con=conect_mysql())
    return df

def pourcentage(df : pd.DataFrame) -> int: 
    '''
    Return percentage of DataFrame
    '''
    somme = 0
    for i in df:
        somme+=i
    try:
        return (somme *100)/len(df)
    except ZeroDivisionError as e:
        raise e

def pourcentage_bikes_district(datemin : str , datemax : str, district : str) -> tuple:
    '''
    Return a tuple (title, plot) of matplotlib plot representing the percentage of ebikes and mechanical bike for all station for one district ('%' district -> All district)
    '''
    fig, ax = plt.subplots()
    
    try:
        df = take_data_date_district('mechanical, ebike', 'station_status', datemin, datemax, district)
        ax.pie(x=[pourcentage(df['mechanical']), pourcentage(df['ebike'])], labels=['mechanical', 'ebike'], explode=(0.01,0.01), autopct = '%1.1f%%')
    except ZeroDivisionError:
        ax.text(0.5, 0.5, 'Any DATA', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

    return ('Pourcentage_bikes_district', fig)

def pourcentage_borne_district (datemin : str , datemax : str, district: str) -> tuple:
    '''
    Return a tuple (title, plot) of matplotlib plot representing the percentage of avalaible and anavalaible dock for all station for one district ('%' district -> All district)
    '''
    fig, ax = plt.subplots()

    try:
        df = take_data_date_district('numdocksavailable, numbikesavailable', 'station_status', datemin, datemax, district)
        ax.pie(x=[pourcentage(df['numdocksavailable']), pourcentage(df['numbikesavailable'])], labels=['dock available', 'bike available'], explode=(0.01,0.01), autopct = '%1.1f%%')
    except ZeroDivisionError:
        ax.text(0.5, 0.5, 'Any DATA', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    return ('Pourcentage_borne_district', fig)

def evol_graph_district(datemin : str , datemax : str, district: str):
    '''
    Return a tuple (title, plot) of matplotlib plot representing evolution of numdocksavailable, numbikesavailable, mechanical, ebike, date- for all station for one district ('%' district -> All district)
    '''
    fig,ax = plt.subplots()
    df =  take_data_date_district('numdocksavailable, numbikesavailable, mechanical, ebike, date', 'station_status', datemin, datemax, district)

    if len(df) == 0:
        ax.text(0.5, 0.5, 'Any DATA', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    else:
        df.plot(ax= ax, x= 'date', ylabel ='Number of bike or dock')
    return ('Evol_graph_district', fig)

def pourcentage_bikes_station (datemin : str , datemax : str, station: str)-> tuple:
    '''
    Return a tuple (title, plot) of matplotlib plot representing the percentage of ebikes and mechanical bike for a specifical station
    '''
    fig, ax = plt.subplots()
    
    try:
        df = take_data_date_station('mechanical, ebike', 'station_status', datemin, datemax, station)
        ax.pie(x=[pourcentage(df['mechanical']), pourcentage(df['ebike'])], labels=['mechanical', 'ebike'], explode=(0.01,0.01), autopct = '%1.1f%%')
    except:
        ax.text(0.5, 0.5, 'Any DATA', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    return ('Pourcentage_bikes_station', fig)

def pourcentage_borne_station (datemin : str , datemax : str, station: str) -> tuple:
    '''
    Return a tuple (title, plot) of matplotlib plot representing the percentage of avalaible and anavalaible dock for a specifical station
    '''
    fig, ax = plt.subplots()
    
    try:
        df = take_data_date_station('numdocksavailable, numbikesavailable', 'station_status', datemin, datemax, station)
        ax.pie(x=[pourcentage(df['numdocksavailable']), pourcentage(df['numbikesavailable'])], labels=['dock available', 'bike available'], explode=(0.01,0.01), autopct = '%1.1f%%')
    except:
        ax.text(0.5, 0.5, 'Any DATA', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    return ('Pourcentage_borne_station', fig)

def evol_graph_station(datemin : str , datemax : str, station: str):
    '''
    Return a tuple (title, plot) of matplotlib plot representing evolution of numdocksavailable, numbikesavailable, mechanical, ebike, date for a specifical station
    '''
    fig,ax = plt.subplots()
    try:
        df =  take_data_date_station('numdocksavailable, numbikesavailable, mechanical, ebike, date', 'station_status', datemin, datemax, station)
    except:
        ax.text(0.5, 0.5, 'Any DATA', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        return ('Evol_graph_station', fig)
        
    if len(df) == 0:
        ax.text(0.5, 0.5, 'Any DATA', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    else:
        df.plot(ax= ax, x= 'date', ylabel ='Number of bike or dock')
    return ('Evol_graph_station', fig)

def graphe_to_img(plot):
    '''
    Save the plot at png image in specifical directory
    '''
    plot[1].savefig(f'./static/maps/img/{plot[0]}.png')

def moyenne(df):
    '''
    Return mean of DataFrame
    '''
    somme = 0
    for i in df:
        somme+=i
    try:
        return round(somme/len(df), 2)
    except ZeroDivisionError as e:
        raise e

if __name__ == '__main__':
    #TEST UNITAIRE
    #print(take_data_date('date, stationcode, ebike', 'station_status','2023-04-12 09:55:13', '2023-04-14 15: 08:59'))
    graphe_to_img(pourcentage_bikes('2023-04-12 09:55:13', '2023-05-16 14:00:00'))
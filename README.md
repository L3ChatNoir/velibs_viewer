# SAE 204

School project that show datas from velib with web application [Django](https://www.djangoproject.com/)

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Views](#views)
- [Contact](#contact)

## Prerequisites

- [WAMP](https://sourceforge.net/projects/wampserver/)
- Library
    - [datetime](https://docs.python.org/3/library/datetime.html)
    - [json](https://docs.python.org/3/library/json.html)
    - [matplotlib.pyplot](https://matplotlib.org/stable/users/installing/index.html)
    - [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
    - [mysql.connector](https://pypi.org/project/mysql-connector-python/)
    - [geopandas](https://geopandas.org/en/stable/getting_started/install.html)
    - [math](https://docs.python.org/3/library/math.html)
    - [shapely.geometry](https://shapely.readthedocs.io/en/stableinstallation.html)
    - [folium and folium.plugins](https://pypi.org/project/folium/)

## Installation

After install all [Prerequisites](#prerequisites) (WAMP + Library), unzip the folder.

### First: Create DATABASE
- Import [sql file](./velibs.sql) in phpmyadmin
- Commented out the 2 lines in the [main file](./sae204/maps/src/main.py) and execute this file. Then re-comment the 2 lines

### Secondly : Launch 
Open terminal and with command line, open the folder ["sae204"](./sae204/)
for example:
```sh
$  cd C:\Users\EXAMPLE\Downloads\SAE204_sources_DUCHANOIS_Lilian_b1\sae204
```

Next, lauch django with command line:
```sh
py .\manage.py runserver
```

## Usage

When application run with Django, open your web browser and go to `http://127.0.0.1:8000/maps/` 

To insert Data to database just execute [main file](./sae204/maps/src/main.py)

All sources file locate in [src folder](./sae204/maps/src)

## Views

In this app, there is 3 views

- View 1: `http://127.0.0.1:8000/maps/accueil/`; This views describe data all station who are in a specifical city
- View 2: `http://127.0.0.1:8000/maps`; show with [OpenStreetMap](https://www.openstreetmap.org) station in map, with the most recent data
- View 3: `http://127.0.0.1:8000/maps/station_data/`; access by `/maps` for use method GET to have stationcode. This views describe data for specifical station

## Contact

[My Github](https://github.com/L3ChatNoir)

My mail: 
>lilian.duchanois@etu.u-pec.fr

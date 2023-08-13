from .db_config import *
from datetime import datetime, timedelta
import folium
import folium.plugins
import json
import geopandas as gpd
from math import sqrt, acos, pi
from shapely.geometry import Polygon, Point
from .data_analiz import *

def map():
    '''
    Save a map (OpenStreetMap) in a html file with a marker for stations, regroup by district of Paris
    '''

    #Récuperation des données utiles
    districts = gpd.read_file("maps/src/arrondissements.geojson")
    df = take_data('stationcode, coordonnees_geo, name', 'station_information')
    df_marker = take_data_lastestdate('stationcode, is_installed, numdocksavailable, numbikesavailable, mechanical, ebike, nom_arrondissement_communes', 'station_status')

    #Création de la map avec le point de vue
    map = folium.Map(location= (48.8362, 2.3428), zoom_start= 11)
    


    
    #Création des point stations rangée dans leur arrondissement respectif

    #Créeation du marker cluster de l'arrondissement
    for i in range(len(districts)):
        mc = folium.plugins.MarkerCluster(name=districts['l_ar'][i]).add_to(map)

        #Si la station est dans l'arrondissement géographique Alors crée le point station avec la fonction create_marker
        #et ajouter dans le marker cluster
        for y in range(len(df)):
            try:
                latlon = json.loads(df.loc[df['stationcode'] == df_marker['stationcode'][y],'coordonnees_geo'].values[0])
                if districts['geometry'][i].contains(Point(latlon['lon'], latlon['lat'])):
                    try:
                        mc.add_child(create_marker(df_marker, y, latlon, df.loc[df['stationcode'] == df_marker['stationcode'][y], 'name'].values[0])).add_to(map)
                    except:
                        mc.add_child(create_marker(df_marker, y, latlon, df_marker['stationcode'][y])).add_to(map)
                    df_marker.drop(index=[y])
            except:
                #print(df_marker['stationcode'][y])
                pass

    #Ajout des control et sauvegarde de la map en html
    folium.LayerControl().add_to(map)
    map.save('./templates/maps/map.html')


def create_marker(df, index, latlon, name) -> folium.Marker:
    '''
        Function that create a folium.Marker and return it
    '''
    
    #Affichage du point différent si station fermé ou station n'ayant plus de vélo disponnible
    info_bulle = ""
    if df["is_installed"][index] == "NON":
            color = "black"
            info_bulle = f"""
            <div>
                <span style="font-size: 13px; padding: 10px;"><b>Cette station est fermé</b></span>
            </div>
            """
    elif df["numbikesavailable"][index] == 0:
        color = "red"
        info_bulle = f"""
        <div>
            <span style="font-size: 13px; padding: 13px;"><b>Aucun vélib disponible</b></span>
        </div>
        """
    else:
        color = "green"
    
    #Création des données afficher lorsqu'on click sur la station
    popup = folium.Popup(f"""
        <center>
            <h3><u>{name}</u></h3>
            {info_bulle}
            <br>
            <br>
            <span style="font-size: 12px; padding: 8px; line-height: 0px; text-size-adjust: auto; white-space: nowrap;">Places disponibles : {df["numdocksavailable"][index]}</span>
            <br>
            <br>
            <br>
            <div>
                <ul>
                    <li><div>
                        <span style="font-size: 13px; padding: 13px;">{df["ebike"][index]} vélib(s) électrique(s)</span>
                    </div></li>
                    <br>
                    <li><div>
                        <span style="font-size: 13px; padding: 13px;">{df["mechanical"][index]} vélib(s) mécanique(s)</span>
                    </div></li>
                </ul>
            </div>
            <form action="station_data/" method="get">
                <input type="hidden" name="station_id" value="{df["stationcode"][index]}"/>
                <input type="submit" value="Information complémentaire" />
            </form>
            <p><b>Station code : {df["stationcode"][index]}</b></p>
        </center>
    """, max_width=700)

    #renvoie le marker
    return folium.Marker(
            location=[latlon['lat'], latlon['lon']],
            popup=popup,
            icon=folium.Icon(
                icon="person-biking",
                prefix='fa',
                color=color
            ),
        )


def point_in_polygon(point : list[float], polygon : list[list[float]]) -> bool:
    '''
    Function return a bool if a point is in a polygon (NOT USE) : la somme des angles du point X à ceux du polygon est congrue à 2kpi avec k impaire
    '''
    def calc_angle_rad(p1 : list, p2 : list, p3 : list):
        a = [p2[0]-p1[0], p2[1]-p1[0]]
        b =  [p3[0]-p1[0], p3[1]-p1[0]]
        ab = a[0]*b[0] + a[1]*a[1]
        normea = sqrt(a[0]**2 + a[1]**2)
        normeb = sqrt(b[0]**2 + b[1]**2)
        return acos((ab/(normea * normeb)*pi)/180)
    
    somme = 0
    for i in range(len(polygon)-1):
        somme += calc_angle_rad(point, [polygon[0][i],  polygon[1][i]], [polygon[0][i+1],  polygon[1][i+1]])

    if (somme / (2 * pi) ) % 2 == 1:    
        return True
    return False


if __name__ == '__main__':
    print(take_data_date('date, stationcode, ebike', 'station_status','2023-04-12 09:55:13', '2023-04-14 15:08:59'))
    map()
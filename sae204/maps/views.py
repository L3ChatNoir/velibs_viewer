from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .src.map import map
from .src.data_analiz import *
from .src.db_config import *
from datetime import datetime, timedelta

def index(request):
    district = request.GET.get('district', '%')
    start_date = request.GET.get('start_date', datetime.strftime(datetime.now().date()- timedelta(days = 7), "%Y-%m-%d" ) )
    end_date = request.GET.get('end_date', datetime.strftime(datetime.now().date(), "%Y-%m-%d"))
    start_time =request.GET.get('start_time', "00:00")
    end_time =request.GET.get('end_time', "23:59")

    df = take_data_date_district('numdocksavailable, numbikesavailable, mechanical, ebike', 'station_status', start_date +" " + start_time + ":00", end_date +" "+ end_time + ":00", district)
    try:
        moy_borne = moyenne(df['numdocksavailable'])
    except ZeroDivisionError:
        moy_borne = 'NO DATA'
    
    try:
        moy_velo = moyenne(df['numbikesavailable'])
    except ZeroDivisionError:
        moy_velo = 'NO DATA'
    
    try:
        moy_ebike = moyenne(df['ebike'])
    except ZeroDivisionError:
        moy_ebike = 'NO DATA'

    try:
        moy_mbike = moyenne(df['mechanical'])
    except ZeroDivisionError:
        moy_mbike = 'NO DATA'

    try:
        moy_capa= moyenne(take_data('capacity', 'station_information')['capacity'])
    except:
        moy_capa= 'NO DATA'
    graphe_to_img(pourcentage_bikes_district(start_date +" " + start_time + ":00", end_date +" "+ end_time + ":00", district))
    graphe_to_img(pourcentage_borne_district(start_date +" " + start_time + ":00", end_date +" "+ end_time + ":00", district))
    graphe_to_img(evol_graph_district(start_date +" " + start_time + ":00", end_date +" "+ end_time + ":00", district))

    if district == '%':
        district = 'All Cities'
    context = {
        'district': district,
        'moy_borne': moy_borne,
        'moy_velo': moy_velo,
        'moy_ebike': moy_ebike,
        'moy_mbike': moy_mbike,
        'start_date': start_date +" " + start_time + ":00",
        'end_date': end_date +" "+ end_time + ":00",
        'moy_capa': moy_capa,
    }

    template = loader.get_template("maps/index.html")
    return HttpResponse(template.render(context, request))

def mappage(request):
    map()
    template = loader.get_template("maps/map.html")
    return HttpResponse(template.render())

def station_data(request):
    stationcode = request.GET.get('station_id', 'NO DATA')
    start_date = request.GET.get('start_date', datetime.strftime(datetime.now().date()- timedelta(days = 7), "%Y-%m-%d" ) )
    end_date = request.GET.get('end_date', datetime.strftime(datetime.now().date(), "%Y-%m-%d"))
    start_time =request.GET.get('start_time', "00:00")
    end_time =request.GET.get('end_time', "23:59")
    
    try:
        df = take_data_date_station('numdocksavailable, numbikesavailable, mechanical, ebike', 'station_status', start_date +" " + start_time + ":00", end_date +" "+ end_time + ":00", stationcode)
        try:
            moy_borne = moyenne(df['numdocksavailable'])
        except ZeroDivisionError:
            moy_borne = 'NO DATA'

        try:
            moy_velo = moyenne(df['numbikesavailable'])
        except ZeroDivisionError:
            moy_velo = 'NO DATA'

        try:
            moy_ebike = moyenne(df['ebike'])
        except ZeroDivisionError:
            moy_ebike = 'NO DATA'

        try:
            moy_mbike = moyenne(df['mechanical'])
        except ZeroDivisionError:
            moy_mbike = 'NO DATA'

        try:
            capa_max = take_data_station('capacity', 'station_information', stationcode).iloc[0][0]
        except:
            capa_max ="NO DATA"
    except:
        moy_borne = 'NO DATA'
        moy_velo = 'NO DATA'
        moy_ebike = 'NO DATA'
        moy_mbike = 'NO DATA'
        capa_max ="NO DATA"
    
    graphe_to_img(pourcentage_bikes_station(start_date +" " + start_time + ":00", end_date +" "+ end_time + ":00", stationcode))
    graphe_to_img(pourcentage_borne_station(start_date +" " + start_time + ":00", end_date +" "+ end_time + ":00", stationcode))
    graphe_to_img(evol_graph_station(start_date +" " + start_time + ":00", end_date +" "+ end_time + ":00", stationcode))

    try:
        nomstation = take_data_station('name', 'station_information', stationcode).iloc[0][0]
    except:
        nomstation = "NO DATA"
 


    template = loader.get_template("maps/views.html")
    context = {
        'stationcode': stationcode,
        'nomstation': nomstation,
        'moy_borne': moy_borne,
        'moy_velo': moy_velo,
        'moy_ebike': moy_ebike,
        'moy_mbike': moy_mbike,
        'capa_max': capa_max,
        'start_date': start_date +" " + start_time + ":00",
        'end_date': end_date +" "+ end_time + ":00",
    }
    return HttpResponse(template.render(context, request))
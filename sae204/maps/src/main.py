from db_config import *

url1 = 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json?lang=fr&timezone=Europe%2FBerlin'
url2 = 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-emplacement-des-stations/exports/json?lang=fr&timezone=Europe%2FBerlin'

#create_table_mysql()
#insert_table_information(urljson_to_df(url2))
update_table_status(1, url1)
import requests
import pandas as pd
from datetime import datetime
import locale
from config import TOMTOM_API_KEY, AIRVISUAL_API_KEY, OPENWEATHER_API_KEY, DIR_REAL_TIME_DATA

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

  
def nearest_street_request(stations2forecast,printData):
    table = pd.read_csv(DIR_REAL_TIME_DATA)
    for station in stations2forecast:
        coordinates = {'MER':{'Station_eqAirVisual': 'MER', 'coordinates':[-99.12766,19.42847]}, "BJU":{'Station_eqAirVisual': 'COYOACAN', 'coordinates':[-99.16174,19.3467]}}
        lat = coordinates[station]['coordinates'][1]
        lon = coordinates[station]['coordinates'][0]
        new_row = {}
        otro_intento = True
        for intentos in range(3):
            if otro_intento ==True:
                url_tomtom = 'https://api.tomtom.com/traffic/services/4/flowSegmentData/relative/16/json?point='+str(lat)+'%2C'+str(lon)+'&unit=KMPH&openLr=false&jsonp=jsonp&key='+ TOMTOM_API_KEY
                response = requests.get(url_tomtom)
                if response.status_code == 200:
                    data_tomtom = response.json()
                    if printData:
                        print(data_tomtom)
                    traffic_flow = data_tomtom.get('flowSegmentData').get('currentSpeed') / data_tomtom.get('flowSegmentData').get('freeFlowSpeed')
                    new_row = {'traffic_flow' : traffic_flow}                    
                        #'frc': data_tomtom.get('flowSegmentData').get('frc'),
                        #'currentSpeed': data_tomtom.get('flowSegmentData').get('currentSpeed'),
                        #'freeFlowSpeed': data_tomtom.get('flowSegmentData').get('freeFlowSpeed'),
                        #'currentTravelTime': data_tomtom.get('flowSegmentData').get('currentTravelTime'),
                        #'freeFlowTravelTime': data_tomtom.get('flowSegmentData').get('freeFlowTravelTime'),
                        #'confidence': data_tomtom.get('flowSegmentData').get('confidence'),
                        #'roadClosure': data_tomtom.get('flowSegmentData').get('roadClosure'),
                    otro_intento = False
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API TomTom. Código de estado: {response.status_code}')
                    
        otro_intento = True
        if station =="MER":
            city = 'Mexico%20City'
        for intentos in range(3):
            if otro_intento ==True:
                url_airvisual = 'http://api.airvisual.com/v2/city?city='+city+'&state=Mexico%20City&country=Mexico&key='+AIRVISUAL_API_KEY
                new_row2 = {}
                response = requests.get(url_airvisual)
                if response.status_code == 200:
                    data_airvisual = response.json()
                    if printData:
                        print(data_airvisual)
                    new_row2 = {
                        'tp': data_airvisual.get('data').get('current').get('weather').get('tp'),
                        'hu': data_airvisual.get('data').get('current').get('weather').get('hu'),
                        'ws': data_airvisual.get('data').get('current').get('weather').get('ws'),
                        'wd': data_airvisual.get('data').get('current').get('weather').get('wd'),
                        }                    
                        #'aqius': data_airvisual.get('data').get('current').get('pollution').get('aqius'),
                        #'mainus': data_airvisual.get('data').get('current').get('pollution').get('mainus'),
                        #'aqicn': data_airvisual.get('data').get('current').get('pollution').get('aqicn'),
                        #'maincn': data_airvisual.get('data').get('current').get('pollution').get('maincn'),
                        #'pr': data_airvisual.get('data').get('current').get('weather').get('pr'),
                        #'ic': data_airvisual.get('data').get('current').get('weather').get('ic')
                    otro_intento = False
                    new_row.update(new_row2)
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API AirVisual. Código de estado: {response.status_code}')

        otro_intento = True
        for intentos in range(3):
            if otro_intento ==True:
                url_openweathermap = 'http://api.openweathermap.org/data/2.5/air_pollution?lat='+str(lat)+'&lon='+str(lon)+'&appid='+OPENWEATHER_API_KEY
                new_row3 = {}
                response = requests.get(url_openweathermap)
                if response.status_code == 200:
                    data_openweather = response.json()
                    if printData:
                        print(data_openweather)
                    new_row3 = {
                        'co': data_openweather.get('list')[0].get('components').get('co'),
                        'no': data_openweather.get('list')[0].get('components').get('no'),
                        'no2': data_openweather.get('list')[0].get('components').get('no2'),
                        'o3': data_openweather.get('list')[0].get('components').get('o3'),
                        'so2': data_openweather.get('list')[0].get('components').get('so2'),
                        'pm2_5': data_openweather.get('list')[0].get('components').get('pm2_5'),
                        'pm10': data_openweather.get('list')[0].get('components').get('pm10'),
                        }
                    otro_intento = False
                    new_row.update(new_row3)
                else:
                    print(f'Error al realizar la solicitud en la estación {station}. API OpenWeather. Código de estado: {response.status_code}')

        if len(new_row) != 0:
            new_row["station"] = station
            datetime_now = datetime.now()
            date = datetime_now.strftime('%Y-%m-%d')
            timestamp = datetime_now.strftime('%H:%M:%S')
            hour = str(datetime_now.hour)
            minute= str(datetime_now.minute)
            new_row['date'] = date
            new_row['timestamp'] = timestamp
            new_row['hour'] = hour
            new_row['minute'] = minute
            # Leer el archivo CSV existente            
            new_row_df = pd.DataFrame([new_row])
            # Añadir la nueva fila al DataFrame usando pd.concat
            df = pd.concat([table, new_row_df], ignore_index=True)                  
            # Escribir el DataFrame actualizado de nuevo al archivo CSV
            df.to_csv(DIR_REAL_TIME_DATA, index=False)
            print(station, "successful request")
    return




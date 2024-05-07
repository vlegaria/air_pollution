from google.protobuf.json_format import MessageToDict
import requests
import matplotlib.pyplot as plt
import numpy as np
import tomtomtrafficflowTile_pb2
import math
import pandas as pd
import schedule
import time
from datetime import datetime, timedelta
import os
import locale

apiKey = "0dR1w4GQ3fKtlRIKGrdiLNmJCQgAZiIC"  
tile = tomtomtrafficflowTile_pb2.Tile()   
tiles_largo = 3
tiles_ancho = 3
zoom_level = 16
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


def tileZXYToLatLon(zoomLevel, x, y):
    MIN_ZOOM_LEVEL = 0
    MAX_ZOOM_LEVEL = 22

    if zoomLevel is None or not isinstance(zoomLevel, (int, float)) or zoomLevel > MAX_ZOOM_LEVEL or zoom_level < MIN_ZOOM_LEVEL:
        raise ValueError(f"Zoom level value is out of range [{MIN_ZOOM_LEVEL}, {MAX_ZOOM_LEVEL}]")
    minXY = 0
    maxXY = int(2**zoomLevel - 1)
    if x is None or not isinstance(x, (int, float)) or x > maxXY or x < minXY:
        raise ValueError(f"Tile x value is out of range [0, {maxXY}]")

    if y is None or not isinstance(y, (int, float)) or y > maxXY or y < minXY:
        raise ValueError(f"Tile y value is out of range [0, {maxXY}]")

    
    lon = (x / (2**zoomLevel)) * (360.0) - (180.0)
    n = (math.pi) - (2.0 * math.pi * y) / (2**zoomLevel)
    lat = (180.0 / math.pi) * (math.atan(0.5 * (math.exp(n) - math.exp(-n))))
   
    return lat,lon

# Función para convertir coordenadas geodésicas a coordenadas de tiles
def latLonToTileZXY(lat, lon, zoom_level):
    MIN_ZOOM_LEVEL = 0
    MAX_ZOOM_LEVEL = 22
    min_lat = -85.051128779807
    max_lat = 85.051128779806
    min_lon = -180.0
    max_lon = 180.0

    # Check input values of zoom level, latitude and longitude
    if (zoom_level is None or not isinstance(zoom_level, (int, float))
        or zoom_level < MIN_ZOOM_LEVEL
        or zoom_level > MAX_ZOOM_LEVEL ):
        
        raise ValueError(
            f"Zoom level value is out of range [{MIN_ZOOM_LEVEL}, {MAX_ZOOM_LEVEL}]"
        )

    if lat is None or not isinstance(lat, (int, float)) or lat < min_lat or lat > max_lat:
        raise ValueError(f"Latitude value is out of range [{min_lat}, {max_lat}]")

    if (lon is None or not isinstance(lon, (int, float))
        or lon < min_lon
        or lon > max_lon ):
        
        raise ValueError(f"Longitude value is out of range [{min_lon}, {max_lon}]")

    z = int(zoom_level)
    xy_tiles_count = 2**z
    x = int(((lon + 180.0) / 360.0) * xy_tiles_count)
    y = int(((1.0 - math.log( math.tan((lat * math.pi) / 180.0) + 1.0 / math.cos((lat * math.pi) / 180.0)) /math.pi)/ 2.0)* xy_tiles_count)

    return x,y

def transform(decodedTiles, zoom_level, xTile, yTile, dataframe=False):
    lat_inicio, lon_inicio = tileZXYToLatLon(zoom_level, xTile, yTile)
    lat_fin, lon_fin = tileZXYToLatLon(zoom_level, xTile+1, yTile+1)

    # Calcular diferencias en latitud y longitud
    diff_lat =lat_fin-lat_inicio
    diff_lon =lon_fin-lon_inicio

    num_pixeles = 4096
    coordinates = []

    # Calcular incrementos por píxel
    inc_lat = diff_lat / num_pixeles
    inc_lon = diff_lon / num_pixeles
    for x,y in decodedTiles:
        lat_pixel = lat_inicio + (y * inc_lat)
        lon_pixel = lon_inicio + (x * inc_lon)
        if dataframe==True:
            coordinates.append([lat_pixel, lon_pixel])
        else:
            coordinates.append((lat_pixel, lon_pixel))
    return coordinates

def decode_geometry(geometry):
    c = 0
    decodeTiles = []
    lines =[]
    decode_x = 0
    decode_y = 0
    while c < len(geometry):
        command_and_count = geometry[c]
        command = command_and_count & 0x7
        count = command_and_count >> 0x3
        for _ in range(count):
            x = geometry[c+1] 
            y = geometry[c+2]
            decode_x += ((x >> 0x1) ^ (-(x & 0x1))) 
            decode_y += ((y >> 0x1) ^ (-(y & 0x1)))
            if command==1:
                if len(decodeTiles)==0:
                    decodeTiles.append([decode_x, decode_y])    
                else:
                    lines.append(decodeTiles) 
                    decodeTiles = []  
                    decodeTiles.append([decode_x, decode_y])    
            elif command==2:     
                decodeTiles.append([decode_x, decode_y])         
            c += 2
        if command==2:
            lines.append(decodeTiles) 
        c += 1        
    return lines



#Para guardarlo como puntos Point debe ser lat, lon
#Si se guardan como líneas linestring, debe ser lon, lat
def conversion_vector(ruta_archivo, zoom_level, xTile, yTile, fecha, hora, estacion):
  #conversion vector a dataframe
  with open(ruta_archivo, "rb") as f:
    tile.ParseFromString(f.read())
  dict_request = MessageToDict(tile)
  points = []
  dictionary ={}
  if "layers" in dict_request.keys():
    if dict_request['layers'][0]['name'] == 'Traffic flow':
      keys = dict_request['layers'][0]["keys"]
      values = dict_request['layers'][0]["values"]
      for line in dict_request['layers'][0]["features"]:
          all_properties = []
          if line["type"]=="LINESTRING":	
            geometry = line["geometry"]
            lines = decode_geometry(geometry)
            for decodedLines in lines:
                coordinates = transform(decodedLines, zoom_level, xTile, yTile)
                if len(coordinates)>0:
                    tags = line["tags"]
                    all_properties = []
                    for i in range(0, int(len(tags)/2), 2):
                        key = keys[tags[i]]
                        value = values[tags[i+1]]
                        value = value[list(value.keys())[0]]
                        properties = {key:value}
                        all_properties.append(properties)

                    dictionary = {"type": line["type"],
                                "properties": all_properties,
                                "coordinates": coordinates,
                                "date": fecha,
                                "time": hora,
                                "station": estacion}
                    points.append(dictionary)
      # Lista de nombres de columnas
      columnas = ['type', 'properties', 'coordinates',"date","time","station"]
      # Crear un DataFrame a partir de la lista y los nombres de columnas
      dataframe = pd.DataFrame(points, columns=columnas)
  else:
     dataframe = []
     points  = []
  return dataframe, points




def conversion_vectorDATAFRAME(ruta_archivo, zoom_level, xTile, yTile, fecha, hora, estacion):
    #conversion vector a dataframe
    with open(ruta_archivo, "rb") as f:
        tile.ParseFromString(f.read())
        dict_request = MessageToDict(tile)
        points = []
        dictionary ={}
        if "layers" in dict_request.keys():
            if dict_request['layers'][0]['name'] == 'Traffic flow':
                keys = dict_request['layers'][0]["keys"]
                values = dict_request['layers'][0]["values"]
                for line in dict_request['layers'][0]["features"]:
                    if line["type"]=="LINESTRING":	
                        geometry = line["geometry"]
                        lines = decode_geometry(geometry)
                        for decodedLines in lines:
                            coordinates = transform(decodedLines, zoom_level, xTile, yTile, dataframe=True)
                            if len(coordinates)>0:
                                tags = line["tags"]
                                all_properties = {}
                                for i in range(0, len(tags), 2):
                                    key = keys[tags[i]]
                                    value = values[tags[i+1]]
                                    value = value[list(value.keys())[0]]
                                    all_properties[key] = value

                                dictionary = {"type": line["type"],
                                            "coordinates": coordinates,
                                            "date": fecha,
                                            "time": hora,
                                            "station": estacion}
                                
                                all_properties.update(dictionary)

                                points.append(all_properties)
                # Lista de nombres de columnas
                columnas = ["type", "road_type", "traffic_level", "traffic_road_coverage", "road_closure", "road_category", "road_subcategory", "left_hand_traffic", "coordinates","date","time","station"]
                # Crear un DataFrame a partir de la lista y los nombres de columnas
                dataframe = pd.DataFrame(points, columns=columnas)
            else:
                dataframe = []
                points  = []
        else:
            dataframe = []
            points  = []

    return dataframe, points



  
def descargar_datos(estaciones, dir_save_vectores, zoom_level):
    global apiKey
    for i in range(len(estaciones)):
        estacion = estaciones.iloc[i]
        nombre = estacion.Key
        tileX = estacion.xTile_in
        tileY = estacion.yTile_in
        if pd.notna(tileX):
            x_tile_in = tileX -1
            x_tile_end = x_tile_in + 3
            y_tile_in = tileY -1
            y_tile_end = y_tile_in + 3
            datetime_now = datetime.now()
            datetime_string = f"{datetime_now.year}_{datetime_now.month:02d}_{datetime_now.day:02d}_{datetime_now.hour:02d}_{datetime_now.minute:02d}_{datetime_now.second:02d}"
            mes = datetime_now.strftime("%B")
            ruta_carpeta = os.path.join(dir_save_vectores, mes)
            if not os.path.exists(ruta_carpeta):
                os.makedirs(ruta_carpeta)
            dia = datetime_now.date()
            ruta_carpeta = os.path.join(ruta_carpeta, str(dia))
            if not os.path.exists(ruta_carpeta):
                os.makedirs(ruta_carpeta)
            hora = str(datetime_now.hour)
            ruta_carpeta = os.path.join(ruta_carpeta, hora)
            if not os.path.exists(ruta_carpeta):
                os.makedirs(ruta_carpeta)
            minuto = str(datetime_now.minute)
            #print(minuto)
            ruta_carpeta = os.path.join(ruta_carpeta, minuto)
            if not os.path.exists(ruta_carpeta):
                os.makedirs(ruta_carpeta)

            x_tile = int(x_tile_in)
            y_tile = int(y_tile_in)
            tiles_largo = 3
            tiles_ancho = 3
            #print(x_tile, y_tile)
            for j in range(tiles_largo):
                x_tile = int(x_tile_in)
                #print("j=",j)
                for k in range(tiles_ancho):
                    otro_intento = True
                    #while(otro_intento==True):
                    for intentos in range(3):
                        if otro_intento ==True:
                            #print("k=",k)
                            url = 'https://api.tomtom.com/traffic/map/4/tile/flow/relative/'+str(zoom_level)+'/'+str(x_tile)+'/'+str(y_tile)+'.pbf?margin=0&tags=%5Broad_type%2Ctraffic_level%2Ctraffic_road_coverage%2Cleft_hand_traffic%2Croad_closure%2Croad_category%2Croad_subcategory%5D&key='+ apiKey
                            #print(url)
                            response = requests.get(url)
                            if response.status_code == 200:
                                nombre_archivo = nombre+"_"+str(int((j*tiles_ancho)+k))+"_"+str(zoom_level)+"_"+str(x_tile) + "_"+ str(y_tile)+"_"+datetime_string+'.pbf'
                                ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
                                with open(ruta_archivo, 'wb') as archivo:
                                        archivo.write(response.content)
                                with open(ruta_archivo, "rb") as f:
                                    tile.ParseFromString(f.read())
                                dict_request = MessageToDict(tile)
                                #print(dict_request)
                                if dict_request['layers'][0]['name'] == 'Traffic flow':
                                    print(f'Archivo guardado como: {ruta_archivo}') 
                                    otro_intento = False
                                else:
                                    os.remove(ruta_archivo)
                                    otro_intento = True
                                    time.sleep(10)   
                            else:
                                print(f'Error al realizar la solicitud. Código de estado: {response.status_code}')
                    x_tile = int(x_tile +1)
                y_tile = int(y_tile +1)
    return
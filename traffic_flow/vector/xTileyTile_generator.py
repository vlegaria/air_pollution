import pandas as pd
import numpy as np
import math
import argparse

# Convierte coordenadas (latitud, longitud) a coordenadas Tiles (específicas de TomTom)
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


def main(args):
    file = args.dirFile
    zoom_level = args.zoom_level
    #zoom_level = 16
    
    df = pd.read_excel(file)
    stationsOfInterest = []
    active = []
    for i in range(len(df)):
        station = df.loc[i]
        params = ["O3", "PM10","PM25"] #lista de parámetros que activan/desactivan contingencias ambientales
        flag = 0 # se pone 0 para iniciar asumiendo que la estación no lee ninguno de los parámetros de interés
        for param in params:
            if not np.isnan(station[param]):
                flag = 1 #Si la estación lee almenos uno de los parámetros de interés, la bandera se activa
        active.append(flag)
        if flag == 1:
            stationsOfInterest.append(station)
    df["active_env_contingency"] = active
    df.to_excel(file, index=False)  # index=False evita escribir el índice en el archivo

    df = pd.read_excel(file)
    for i in range(len(df)):
        station = df.loc[i]
        if station["active_env_contingency"] == 1: #es una estación de interés porque activa/desactiva contingencias
            latitude = station.Latitude
            longitude = station.Longitude
            if pd.notna(latitude) and pd.notna(longitude):
                tileX, tileY = latLonToTileZXY(latitude, longitude, zoom_level)
                df.at[i,"xTile_in"] = tileX
                df.at[i,"yTile_in"] = tileY
    df.to_excel(file, index=False)  # index=False evita escribir el índice en el archivo


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirFile", default='C:/Users/valer/Documents/CIC/doctorado/air_pollution/traffic_flow/vector/estaciones.xlsx', help="file with location of monitoring stations")
    parser.add_argument("--zoom_level", default=16, type=int, help="do not modify unless necessary")
    args = parser.parse_args()
    main(args)

#ejecutar con la ubicación de archivo por default 
#python xTileyTile_generator.py

#ejectuar con una nueva dirección
#python xTileyTile_generator.py --dirFile "C:/Users/.../estaciones.xlsx"
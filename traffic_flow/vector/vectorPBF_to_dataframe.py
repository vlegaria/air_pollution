from google.protobuf.json_format import MessageToDict
import pandas as pd
import math
import geopandas as gpd
from shapely.geometry import LineString, Point
import tomtomtrafficflowTile_pb2
import os
import matplotlib.pyplot as plt
import numpy as np
import argparse
from utils_TomTom import *
def main(args):
    # Valores globales
    zoom_level = 16
    tile = tomtomtrafficflowTile_pb2.Tile()
    tiles_largo = 3
    tiles_ancho = 3

    #month = "junio"
    month = args.month
    #ruta_raiz = "C:/Users/.../air_pollution_data/vectores/"+month+"/"
    ruta_raiz = "C:/Users/valer/Documents/CIC/doctorado/air_pollution_data/vectores/"+month+"/"
    dataframes = []
    all_points = []
    # Itera sobre todas las carpetas y subcarpetas
    for carpeta_actual, carpetas, archivos in os.walk(ruta_raiz):
        # Itera sobre todos los archivos en la carpeta actual
        for nombre_archivo in archivos:
            # Forma la ruta completa del archivo
            ruta_archivo = os.path.join(carpeta_actual, nombre_archivo)
            
            # Verifica si el archivo tiene una extensión específica (por ejemplo, .xlsx)
            if nombre_archivo.endswith('.pbf'):
                # Lee el archivo y agrega el DataFrame a la lista
                nombre = nombre_archivo.split("_")
                zoom_level = int(nombre[2])
                xTile = int(nombre[3])
                yTile = int(nombre[4])
                fecha = nombre[7]+"-"+nombre[6]+"-"+nombre[5]
                ultimo = nombre[10].split(".")
                hora = nombre[8]+":"+nombre[9]+":"+ultimo[0]
                estacion = nombre[0]
                dataframe, points = conversion_vectorDATAFRAME(ruta_archivo, zoom_level, xTile, yTile, fecha, hora, estacion)

                if len(dataframe)>0:
                    dataframes.append(dataframe)
                    all_points.append(points)

    # Combina todos los DataFrames en uno solo
    df_completo = pd.concat(dataframes, ignore_index=True)
    df_name = month+".csv"
    # Muestra el DataFrame completo
    df_completo.to_csv(df_name, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("--dirFile", default='C:/Users/valer/Documents/CIC/doctorado/air_pollution/traffic_flow/vector/estaciones.xlsx', help="file with location of monitoring stations")
    parser.add_argument("-m", "--month", type=str, help="month")
    args = parser.parse_args()
    main(args)
    
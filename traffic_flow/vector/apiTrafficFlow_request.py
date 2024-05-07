import pandas as pd
import time
from datetime import datetime
import argparse
from utils_TomTom import *


locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def main(args):
    file = args.dirFile
    zoom_level = 16
    dir_save_vectores = "vectores"
    df = pd.read_excel(file)
    #Ignora las filas con datos faltantes en la columna de xTile_in (i.e. solo toma en cuenta las estaciones de las que se conoce su ubicación)
    estaciones = df.dropna(subset=['xTile_in'])
    estaciones = estaciones.reset_index()
    del estaciones["index"]
    print("Numero de estaciones a consultar:",len(estaciones))

    while True:
        hora_actual = datetime.now()
        hora = str(hora_actual.hour)
        minuto = str(hora_actual.minute)
        print(hora, minuto)
        if minuto == "9":
            try:
                descargar_datos(estaciones, dir_save_vectores, zoom_level)
            except:
                print("No se descargaron datos a las: ", hora,":", minuto)
        if minuto == "11":
            try:
                descargar_datos(estaciones, dir_save_vectores, zoom_level)
            except:
                print("No se descargaron datos a las: ", hora,":", minuto)
        if minuto == "26":
            try:
                descargar_datos(estaciones, dir_save_vectores, zoom_level)
            except:
                print("No se descargaron datos a las: ", hora,":", minuto)
        if minuto == "54":
            try:
                descargar_datos(estaciones, dir_save_vectores, zoom_level)
            except Exception as e:
                print("No se descargaron datos a las: ", hora,":", minuto)
                print("Ocurrió una excepción:", e)

        time.sleep(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirFile", default='C:/Users/valer/Documents/CIC/doctorado/air_pollution/traffic_flow/vector/estaciones.xlsx', help="file with location of monitoring stations")
    args = parser.parse_args()
    main(args)

    
#ejecutar con la ubicación de archivo por default 
#cd Documents/CIC/doctorado/air_pollution/traffic_flow/vector
#python apiTrafficFlow_request.py

#ejectuar con una nueva dirección
#python apiTrafficFlow_request.py --dirFile "C:/Users/.../estaciones.xlsx"
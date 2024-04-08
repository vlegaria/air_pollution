# Cambiar el nombre de todos los archivos en una carpeta
# Agrega el nombre (CÓDIGO) de la estacion de donde provienen los csv descargados de la página de SINAICA
import os
import pandas as pd
import argparse


def main(args):
    try: 
        directory = args.dir
        string = args.str2add
        filenames = os.listdir(directory)
        for filename in filenames:
            new_filename = filename.replace('.csv', '') + "_" + string +".csv"
            # Ruta completa de los archivos original y nuevo
            ruta_original = os.path.join(directory, filename)
            ruta_nuevo = os.path.join(directory, new_filename)
            # Renombrar el archivo
            os.rename(ruta_original, ruta_nuevo)
        print("Success")
    except:
        print("Process fail")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, default=os.getcwd(), type=str, help="folder with files to rename")
    parser.add_argument("--str2add", required=True, default=os.getcwd(), type=str, help="string to add at the end of all csv from the same measuremnt station")
    args = parser.parse_args()
    main(args)

# python rename_files.py --dir "C:/Users/all_csv/" --str2add "MER"
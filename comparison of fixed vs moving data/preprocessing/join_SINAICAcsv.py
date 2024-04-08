# Script to consolidate all CSV files downloaded from SINAICA's repository, containing measurements from fixed stations collecting air pollution and temperature data
import argparse
import pandas as pd
import os
from unidecode import unidecode
import numpy as np
def main(args):
    try: 
        directory = args.dirIn
        filename_dirOut = args.dirOut
        files = os.listdir(directory)
        df = pd.DataFrame()
        for file in files:
            content = pd.read_csv(directory+'/'+file)
            filename = file.replace('.csv', '')
            content["Codigo_estacion"] = filename.rsplit('_', 1)[-1]
            df = pd.concat([df, content], ignore_index=True)
        df.drop_duplicates(inplace=True)
        df = df.reset_index(drop=True)
        headings_without_accents = [unidecode(string) for string in list(df.columns)]
        df.columns = headings_without_accents
        #df_reset[["start_time", "final_time"]] = df_reset.Hora.str.split('-', expand=True)
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')

        # Crear columnas separadas para año, mes y día
        df['year'] = df['Fecha'].dt.year
        df['month'] = df['Fecha'].dt.month
        df['day'] = df['Fecha'].dt.day
        df[['start_hour', 'final_hour']] = df['Hora'].str.split(' - ', expand=True)
        df[['start_hour', 'start_minute']] = df['start_hour'].str.split(':', expand=True)
        df[['final_hour', 'final_minute']] = df['final_hour'].str.split(':', expand=True)
        df['start_seconds'] = np.zeros(len(df))
        #df_reset[["start_time", "final_time"]] = df_reset.start_time.str.split(':', expand=True)
        df.to_csv(filename_dirOut, encoding='latin-1', index=False)
        #df_reset.to_csv(filename_dirOut)
        print("Success")
    except:
        print("Process fail")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirIn", required=True, default=os.getcwd(), type=str, help="folder with csv's from SINAICA")
    parser.add_argument("--dirOut", required=True, default=os.getcwd(), type=str, help="output file address")
    args = parser.parse_args()
    main(args)

# python join_SINAICAcsv.py --dirIn "C:/Users/all_csv/" --dirOut "C:/Users/all_csv/Output_file.csv"
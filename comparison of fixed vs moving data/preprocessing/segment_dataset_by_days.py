# Segmentation of the dataset by days for visualization in QGIS
import pandas as pd
import argparse
import numpy as np
import os

string_months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        
def main(args):
    try: 
        dirIn = args.dirIn
        dirOut = args.dirOut
        if not os.path.exists(dirOut):
            os.makedirs(dirOut)
            print(f"Folder created at output address")
        df = pd.read_csv(dirIn)
        for year in df["ao"].unique():
            data_by_year = df[df["ao"]==year]
            for month in df["mes"].unique():
                data_by_month = data_by_year[data_by_year["mes"]==month]
                days = np.sort(list(data_by_month["dia"].unique()))
                for day in days:
                    #print(month, day, ',', day,': with ', len(data_by_month[data_by_month["dia"]==day]), 'instances')
                    file_length = len(data_by_month[data_by_month["dia"]==day])
                    file_name = string_months[month]+"_"+str(day)+"_"+str(year)+".csv"
                    file_dir = os.path.join(dirOut, file_name)
                    if os.path.exists(file_name):
                        print(f"File with name {file_name} already exists")
                    else:
                        print(f"Saving file {file_name} with {file_length} instances")
                        data_by_month[data_by_month["dia"]==day].to_csv(file_dir)
    except Exception as e:
        print("Process fail", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirIn", required=True, type=str, help="input file address to segment by days")
    parser.add_argument("--dirOut", required=True, type=str, help="output file address")
    args = parser.parse_args()
    main(args)


# Run script as: python segment_dataset_by_days.py --dirIn "C:/Users/---/data.csv" --dirOut "C:/Users/---/datos/segment_files"

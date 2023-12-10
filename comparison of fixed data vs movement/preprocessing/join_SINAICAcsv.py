# Script to consolidate all CSV files downloaded from SINAICA's repository, containing measurements from fixed stations collecting air pollution and temperature data
import argparse
import pandas as pd
import os

def main(args):
    try: 
        directory = args.dir
        files = os.listdir(directory)
        df = pd.DataFrame()
        for file in files:
            content = pd.read_csv(directory+'/'+file)
            filename = file.replace('.csv', '')
            content["Codigo_estacion"] = filename.rsplit('_', 1)[-1]
            df = pd.concat([df, content], ignore_index=True)
        df.drop_duplicates(inplace=True)
        df_reset = df.reset_index(drop=True)
        df_reset.to_csv("all_csv.csv")
        print("Success")
    except:
        print("Process fail")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, default=os.getcwd(), type=str, help="folder with csv's from SINAICA")
    args = parser.parse_args()
    main(args)

# directory = python join_SINAICAcsv.py --dir "C:/Users/---/datos"
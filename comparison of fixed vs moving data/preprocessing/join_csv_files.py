# Script to join all CSV files in one
import pandas as pd
import os
import argparse

def main(args):
    try: 
        directory = args.dirIn
        filename = args.dirOut
        files = os.listdir(directory)
        df = pd.DataFrame()
        for file in files:
            content = pd.read_csv(directory+'/'+file)
            df = pd.concat([df, content], ignore_index=True)
        df.drop_duplicates(inplace=True)
        df_reset = df.reset_index(drop=True)
        df_reset.to_csv(filename)
        print("Success")
    except:
        print("Process fail")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirIn", required=True, default=os.getcwd(), type=str, help="input file address to segment by days")
    parser.add_argument("--dirOut", required=True, default=os.getcwd(), type=str, help="output file address")
    args = parser.parse_args()
    main(args)

# directory = python join_csv_files.py --dirIn "C:/Users/all_csv/" --dirOut "C:/Users/all_csv/Output_file.csv"
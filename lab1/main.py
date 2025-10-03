import pandas as pd
import numpy as np
import os
import random
from concurrent.futures import ProcessPoolExecutor as Pool

#const values
CATEGORIES = ['A', 'B', 'C', 'D']
NUM_FILES = 5
ROWS_IN_FILE = 100
OUTPUT_PATH = "output"

#generation csv files
def generate_csv_files():
    os.makedirs(OUTPUT_PATH, exist_ok = True)

    for i in range(NUM_FILES):
        categories = []
        values = []

        for j in range(ROWS_IN_FILE):
            category = random.choice(CATEGORIES)
            value = round(random.uniform(1.0, 100.0), 2)
            categories.append(category)
            values.append(value)
        
        data = {"Category" : categories, "Value" : values}
        df = pd.DataFrame(data)
        file_name = f"file_{i+1}.csv"
        file_path = OUTPUT_PATH + '\\' + file_name
        df.to_csv(file_path, index=False)

#first file processing
def process_file(file_path):
    df = pd.read_csv(file_path)
    medians = []
    stds = []
    categories = []

    for category in CATEGORIES:
        categories.append(category)
        values = df[df["Category"] == category]["Value"]
        
        if not values.empty:
            median = round(values.median(), 2)
            std = round(values.std(), 2)
            medians.append(median)
            stds.append(std)
        else:
            medians.append(None)
            stds.append(None)
    result = {"Category" : categories, "Median" : medians, "Std" : stds}
    file_name = file_path.replace(".csv", "_out.csv")
    df = pd.DataFrame(result).to_csv(file_name, index=False)
        
def parallel_processing():
    files = []
    for i in range(NUM_FILES):
        files.append(f"{OUTPUT_PATH}\\file_{i+1}.csv")
    
    with Pool(NUM_FILES) as pool:
        pool.map(process_file, files)

#second processing
def final_processing():
    all_median = {}
    all_std = {}
    all_medians_of_medians = []
    all_std_of_medians = []
    result = {}
    for c in CATEGORIES:
        all_median[c] = []
        all_std[c] = []

    for i in range(NUM_FILES):
        df = pd.read_csv(f"{OUTPUT_PATH}\\file_{i+1}_out.csv")
        for c in CATEGORIES:
            all_median[c].append(df.loc[df["Category"] == c, "Median"])
            all_std[c].append((df[df["Category"] == c]["Std"]))
    
    for c in CATEGORIES:
        all_medians_of_medians.append(round(np.median(all_median[c]), 2))
        all_std_of_medians.append(round(np.std(all_median[c]), 2))   
     
    data = {"Category" : CATEGORIES, "Median of medians" : all_medians_of_medians, "Std of medians" : all_std_of_medians}
    df = pd.DataFrame(data).to_csv(f"{OUTPUT_PATH}\\final_out.csv", index=False) 

#main part
if __name__ == '__main__':
    generate_csv_files()
    parallel_processing()
    final_processing()
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.join(current_dir, '..')
sys.path.append(script_dir)

import download_file_s3
import get_unique_wells

import get_well_data
import pandas as pd
import insert_into_db



if __name__ == "__main__":
    get_unique_wells.get_unique_wells('Groundwater2024-05-25.xlsx')
    unique_wells = pd.read_csv('./unique_wells.csv', header=None)
    unique_wells = unique_wells.iloc[0].to_list()
    for code in unique_wells:
        get_well_data.get_and_download_well_info(code)
        insert_into_db.insert_into_db(file_name=f'{code.replace('/', '-')}.csv')

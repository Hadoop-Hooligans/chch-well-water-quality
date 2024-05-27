import sys
import os
import get_csv_v2

current_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.join(current_dir, '..')
sys.path.append(script_dir)

# import download_file_s3
import get_unique_wells
import get_into_dataframe

# import get_well_data
import pandas as pd
# import insert_into_db



if __name__ == "__main__":
    get_unique_wells.get_unique_wells('Groundwater2024-05-25.xlsx')
    unique_wells = pd.read_csv('./unique_wells.csv', header=None)
    unique_wells = unique_wells.iloc[0].to_list()
    code_to_test = 'BT27/5037'
    get_csv_v2.get_csv_file(well_code=code_to_test)
    get_into_dataframe.get_main_data(well_code=code_to_test)

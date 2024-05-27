import pandas as pd
import download_file_s3
import upload_file_s3
import csv

def get_unique_wells(file_path):
    # Load the Excel file
    download_file_s3.download_file_s3(file_name=file_path)
    lawa_well = pd.read_excel(file_path, sheet_name=1)
    lawa_well_chch = lawa_well[lawa_well['Region'] == 'Canterbury']
    chch_unique_wells = list(lawa_well_chch['LAWAWellName'].unique())
    with open('unique_wells.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(chch_unique_wells)
    upload_file_s3.upload_file_s3('./unique_wells.csv')


import os
import requests

def download_excel_workbook(url, ID):
    """Takes the url of the direct csv download link (and the ID) and downloads the csv into a folder called well_data"""
    directory = os.getcwd()
    if not os.path.basename(directory) == 'well_data':
        os.makedirs('well_data', exist_ok=True)
        os.chdir('well_data')
        directory = os.getcwd()

    print(f"Downloading content from {url}")
    response = requests.get(url)
    print(url.endswith)
    new_id = ID.replace('/', '-')
    file_path = os.path.join(directory, f'{new_id}.csv')
    with open(file_path, 'wb') as f: #Its safer to write the dataset to disk first, then read it into pandas
                f.write(response.content)
    return 1

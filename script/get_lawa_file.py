import pandas as pd
from datetime import date
import os
import requests

def download_excel_workbook(url, name="Groundwater") -> dict:
    """Function that takes the url download link of a file, and then returns a dictionary of worksheet:pandas df pairs"""
    print(f"Downloading content from {url}")
    response = requests.get(url)
    content_type = response.headers.get('Content-Type')
    assert 'excel' in content_type or url.endswith(('.xls', '.xlsx'))
    file_dest = "LawaDownloads"
    os.makedirs(file_dest, exist_ok=True)

    save_path = os.path.join(file_dest, name + str(date.today()) + ".xlsx")
    with open(save_path, 'wb') as f: #Its safer to write the dataset to disk first, then read it into pandas
                f.write(response.content)
    print("File written")
    return save_path

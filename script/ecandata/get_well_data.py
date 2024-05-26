import get_csv_file
import get_csv_download_link
import get_observation_link
import time


SCRAP_DELAY = 2  #seconds

def get_and_download_well_info(code):
    """Main function for this script, brings everyone together. Given a list-like of well codes, it will create a folder called well_data and download the most recent csv reports into that folder"""
    time.sleep(SCRAP_DELAY) # don't get banned that would be bad
    try:
        well_link, ID = get_observation_link.get_obs_link(code)
        csv_link, ID = get_csv_download_link.get_csv_download_link(well_link, ID)
        get_csv_file.download_excel_workbook(csv_link, ID)
    except Exception as e:
            print(f"There was an error: {e} when trying to download the code: {code}")
    return 1


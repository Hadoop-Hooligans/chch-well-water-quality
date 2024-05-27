import encode_well
import requests

def get_csv_file(well_code):
    # Get the observation link
    # url, id = get_obs_link(well_code)
    # Encode the well code
    # url = encode_well.encode_well(well_code)

    all_well_data = f"https://www.ecan.govt.nz/data/water-quality-data/exportallsample/{well_code.replace('/', '_')}"
    response = requests.get(all_well_data)
    filename = f"{well_code.replace('/', '_')}.csv"
    with open(
        f"./{filename}", "wb"
    ) as f:  # Its safer to write the dataset to disk first, then read it into pandas
        f.write(response.content)

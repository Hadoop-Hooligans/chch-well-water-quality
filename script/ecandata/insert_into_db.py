import sys
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.join(current_dir, '..')
sys.path.append(script_dir)

import pandas as pd
import connect_to_db

def insert_into_db(file_name):
    try:
        well_info = pd.read_csv(file_name, nrows=4, header=None)
        well_dict = well_info.set_index(0).to_dict()[1]
        date_obj = datetime.strptime(well_dict['Collection Date'], '%d-%b %Y %H:%M%p')
        formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        well_dict['Collection Date'] = formatted_date

        parameters_info = pd.read_csv(file_name, skiprows=4)
        parameters_info = parameters_info.transpose()
        parameters_info.columns = parameters_info.iloc[0]

    except FileNotFoundError:
        print(f'Well {file_name} not found. Skipping')

    connection = connect_to_db.connect_to_database()
    insert_into_recordings(connection, well_dict, parameters_info)



def insert_into_recordings(conn, well_info_row, parameters_info_row):
    try:
        cur = conn.cursor()
        select_query = '''
        SELECT 1 FROM sample WHERE sample_id = %s;
        '''
        cur.execute(select_query, (well_info_row["Sample ID"],))
        if cur.fetchone() is None:
            # Data does not exist, perform the insert
            insert_query = '''
            INSERT INTO recordings
            (
                well_id,
                sample_id,
                recording_date
            )
            VALUES
            (
                %s, %s, %s
            );
            '''
            cur.execute(insert_query, (
                well_info_row["Site ID"],
                well_info_row["Sample ID"],
                well_info_row["Collection Date"]
            ))
            insert_into_sample(conn, parameters_info_row, well_info_row["Sample ID"], well_info_row["Collection Date"])
            conn.commit()
            print(f"Data inserted")
        else:
            print(f"Data already exists, skipping insertion.")
            cur.close()
    except Exception as e:
        print(f"Error Inserting Data: {e}")


def insert_into_sample(conn, row, sample_id, date_recorded):
    try:
        cur = conn.cursor()
            # Data does not exist, perform the insert
        insert_query = '''
        INSERT INTO sample
        (
            sample_id,
            date_recorded,
            chloride,
            hardness_total,
            calcium,
            ph,
            ph_field,
            sodium_dissolved,
            sulphate,
            water_temperature,
            oxygen_dissolved,
            magnesium,
            silica,
            nitrate_nitrogen,
            e_coli,
            total_coliforms
        )
        VALUES
        (
            %s,
            %s,
            (%s)::actual_determinand,
            (%s)::actual_determinand,
            (%s)::actual_determinand,
            (%s)::actual_determinand,
            (%s)::actual_determinand,
            (%s)::actual_determinand,
            (%s)::actual_determinand,
            (%s)::actual_determinand,
            (%s)::actual_determinand,
            (%s)::actual_determinand,
            (%s)::actual_determinand,
            (%s)::actual_determinand,
            (%s)::actual_determinand,
            (%s)::actual_determinand
        );
        '''
        cur.execute(insert_query, (
            sample_id,
            date_recorded,
            (row.get("Chloride").get("Name"), row.get("Chloride").get("Value"), row.get("Chloride").get("Units")),
            (row.get("Hardness, Total").get("Name"), row.get("Hardness, Total").get("Value"), row.get("Hardness, Total").get("Units")),
            (row.get("Calcium, Dissolved").get("Name"), row.get("Calcium, Dissolved").get("Value"), row.get("Calcium, Dissolved").get("Units")),
            (row.get("pH").get("Name"), row.get("pH").get("Value"), row.get("pH").get("Units")),
            (row.get("pH (Field)").get("Name"), row.get("pH (Field)").get("Value"), row.get("pH (Field)").get("Units")),
            (row.get("Sodium, Dissolved").get("Name"), row.get("Sodium, Dissolved").get("Value"), row.get("Sodium, Dissolved").get("Units")),
            (row.get("Sulphate").get("Name"), row.get("Sulphate").get("Value"), row.get("Sulphate").get("Units")),
            (row.get("Water Temperature (Field)").get("Name"), row.get("Water Temperature (Field)").get("Value"), row.get("Water Temperature (Field)").get("Units")),
            (row.get("Dissolved Oxygen").get("Name"), row.get("Dissolved Oxygen").get("Value"), row.get("Dissolved Oxygen").get("Units")),
            (row.get("Magnesium, Dissolved").get("Name"), row.get("Magnesium, Dissolved").get("Value"), row.get("Magnesium, Dissolved").get("Units")),
            (row.get("Silica, Reactive").get("Name"), row.get("Silica, Reactive").get("Value"), row.get("Silica, Reactive").get("Units")),
            (row.get("Nitrate Nitrogen").get("Name"), row.get("Nitrate Nitrogen").get("Value"), row.get("Nitrate Nitrogen").get("Units")),
            (row.get("E. coli").get("Name"), row.get("E. coli").get("Value"), row.get("E. coli").get("Units")),
            (row.get("Total Coliforms").get("Name"), row.get("Total Coliforms").get("Value"), row.get("Total Coliforms").get("Units"))
        ))
        conn.commit()
        print(f"Data inserted")
        cur.close()
    except Exception as e:
        print(f"Error Inserting Data: {e}")


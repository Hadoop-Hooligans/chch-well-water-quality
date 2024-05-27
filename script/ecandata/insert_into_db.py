import sys
import os
from datetime import datetime
import json


current_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.join(current_dir, '..')
sys.path.append(script_dir)

import pandas as pd
import connect_to_db

def get_measurement_value(df, measurement):
    row = df[df['Measurement'] == measurement]
    if not row.empty:
        value = row.iloc[0]['Value']
        units = row.iloc[0]['Units']
        return {"determinand_name" : str(measurement),
                "determinand_actual_value" : str(value),
                "determinand_units" : str(units)
                }
    else:
        return {"determinand_name" : None,
                "determinand_actual_value" : None,
                "determinand_units" : None
                }



def insert_into_db(well_code, sample, collection_date ,sub_df):
    connection = connect_to_db.connect_to_database()
    insert_into_recordings(conn=connection, well_code=well_code, sample= sample, collection_date=collection_date, sub_df=sub_df)



def insert_into_recordings(conn, well_code, sample, collection_date, sub_df):
    try:
        cur = conn.cursor()
        select_query = '''
        SELECT 1 FROM recordings WHERE sample_id = %s;
        '''
        cur.execute(select_query, (str(sample),))
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
                well_code,
                str(sample),
                collection_date
            ))
            insert_into_sample(conn=conn, sample_id=sample, collection_date=collection_date, sub_df= sub_df)
            conn.commit()
            print(f"Data inserted")
        else:
            print(f"Data already exists, skipping insertion.")
            cur.close()
    except Exception as e:
        print(f"Error Inserting Data: {e}")


def insert_into_sample(conn, sample_id, collection_date, sub_df):
    try:
        cur = conn.cursor()
            # Data does not exist, perform the insert
        insert_query = '''
        INSERT INTO sample_v2
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
            %s::jsonb,
            %s::jsonb,
            %s::jsonb,
            %s::jsonb,
            %s::jsonb,
            %s::jsonb,
            %s::jsonb,
            %s::jsonb,
            %s::jsonb,
            %s::jsonb,
            %s::jsonb,
            %s::jsonb,
            %s::jsonb,
            %s::jsonb
        );
        '''
        chloride = get_measurement_value(sub_df, 'Chloride')
        hardness_total = get_measurement_value(sub_df, 'Hardness, Total')
        calcium = get_measurement_value(sub_df, 'Calcium, Dissolved')
        ph = get_measurement_value(sub_df, 'pH')
        ph_field = get_measurement_value(sub_df, 'pH (Field)')
        sodium_dissolved = get_measurement_value(sub_df, 'Sodium, Dissolved')
        sulphate = get_measurement_value(sub_df, 'Sulphate')
        water_temperature = get_measurement_value(sub_df, 'Water Temperature (Field)')
        oxygen_dissolved = get_measurement_value(sub_df, 'Dissolved Oxygen')
        magnesium = get_measurement_value(sub_df, 'Magnesium, Dissolved')
        silica = get_measurement_value(sub_df, 'Silica, Reactive')
        nitrate_nitrogen = get_measurement_value(sub_df, 'Nitrate Nitrogen')
        e_coli = get_measurement_value(sub_df, 'E. coli')
        total_coliforms = get_measurement_value(sub_df, 'Total Coliforms')

        cur.execute(insert_query, (
            str(sample_id),
            collection_date,
            json.dumps(chloride),
            json.dumps(hardness_total),
            json.dumps(calcium),
            json.dumps(ph),
            json.dumps(ph_field),
            json.dumps(sodium_dissolved),
            json.dumps(sulphate),
            json.dumps(water_temperature),
            json.dumps(oxygen_dissolved),
            json.dumps(magnesium),
            json.dumps(silica),
            json.dumps(nitrate_nitrogen),
            json.dumps(e_coli),
            json.dumps(total_coliforms)
        ))
        conn.commit()
        print(f"Data inserted")
        cur.close()
    except Exception as e:
        print(f"Error Inserting Data: {e}")

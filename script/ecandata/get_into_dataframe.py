import pandas as pd
from datetime import datetime
import change_date_time_format
import insert_into_db



def get_main_data(well_code):
    main_df = pd.read_csv(f'{well_code.replace('/', '_')}.csv', skiprows=2)
    main_df['SampleID'] = main_df['SampleID'].astype(str)
    main_df['Collection Date'] = main_df['Collection Date'].apply(change_date_time_format.change_date_time_format)

    samples = main_df['SampleID'].unique()

    for sample in samples:
        if sample != 'nan':
            # print(sample)
            sub_df = main_df[main_df['SampleID'] == sample]
            insert_into_db.insert_into_db(well_code=well_code, sample=sample, collection_date=sub_df['Collection Date'].iloc[0] ,sub_df=sub_df)

        # insert_into_db.insert_into_recordings(well_code, sample, sub_df['Collection Date'][0])
        # sub_df.apply(insert_into_db.insert_into_sample, axis=1)




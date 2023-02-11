import pandas as pd


def extract_name_coor(df: pd.DataFrame):
    df1 = df.query('longitude > -1' and 'latitude > -1').groupby(['name', 'latitude', 'longitude']).first().sort_values(
        by=['_id']).reset_index()

    return df1[['name', 'latitude', 'longitude']]
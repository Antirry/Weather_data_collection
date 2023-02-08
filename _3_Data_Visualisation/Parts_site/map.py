import folium
import pandas as pd


def extract_name_coor(df: pd.DataFrame):
    df1 = df.query('longitude > -1' and 'latitude > -1').groupby(['name', 'latitude', 'longitude']).first().sort_values(
        by=['_id']).reset_index()

    df2 = df1[['latitude', 'longitude']].values.tolist()
    df_coor = [coor for coor in df2]

    df3 = df1['name'].tolist()
    df_name = [name for name in df3]

    return [df_name, df_coor]


def my_map(extract_name_coor_: list):
    names, coordinates = extract_name_coor_

    m = folium.Map(location=[64.6863136, 97.7453061],  # широта и долгота России
                   zoom_start=4)

    feature_group = folium.FeatureGroup("Marks")
    for name, coordinate in zip(names, coordinates):
        feature_group.add_child(folium.Marker(location=coordinate, popup=name))

    m.add_child(feature_group)

    return m


def main_map(df: pd.DataFrame):
    return my_map(extract_name_coor(df))

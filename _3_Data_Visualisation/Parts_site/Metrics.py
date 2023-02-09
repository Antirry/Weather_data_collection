import pandas as pd


def mean_temp_min(df: pd.DataFrame):
    mean_temp = df.groupby('name')['temp'].mean().reset_index(name='temp')
    mean_temp_min = mean_temp.loc[mean_temp['temp'].idxmin(), ['name', 'temp']]
    return [mean_temp_min['name'], round(mean_temp_min['temp'], 2), mean_temp]


def mean_data(df: pd.DataFrame, mean_temp_name):
    mean_temp_accuracy_ = df.groupby('name')[['temp_max', 'temp_min']].mean().reset_index()
    mean_temp_accuracy_name = mean_temp_accuracy_.loc[mean_temp_accuracy_['name'] == mean_temp_name]
    mean_temp_accuracy_sub = mean_temp_accuracy_name['temp_max'] - mean_temp_accuracy_name['temp_min']
    return [mean_temp_accuracy_name, mean_temp_accuracy_sub]


def mean_temp_accuracy_min(mean_temp_accuracy_name, mean_temp_accuracy_sub):
    mean_temp_accuracy_name = mean_temp_accuracy_name['name'].item()
    mean_temp_accuracy_sub = round(mean_temp_accuracy_sub.item(), 2)
    return [mean_temp_accuracy_name, mean_temp_accuracy_sub]


def mean_temp_max(mean_temp):
    mean_temp_max_ = mean_temp.loc[mean_temp['temp'].idxmax(), ['name', 'temp']]
    return [mean_temp_max_['name'], round(mean_temp_max_['temp'], 2)]


def mean_temp_accuracy_max(mean_temp_accuracy_name, mean_temp_accuracy_sub):
    mean_temp_accuracy_name = mean_temp_accuracy_name['name'].item()
    mean_temp_accuracy_sub = round(mean_temp_accuracy_sub.item(), 2)
    return [mean_temp_accuracy_name, mean_temp_accuracy_sub]


def mean_wind(df: pd.DataFrame):
    mean_wind_ = df.groupby('name')['wind'].mean().reset_index(name='wind')
    mean_wind_max = mean_wind_.loc[mean_wind_['wind'].idxmax(), ['name', 'wind']]
    return [mean_wind_max['name'], round(mean_wind_max['wind'], 2)]


def metrics(df: pd.DataFrame):
    name_mean_temp_min, round_mean_temp_min, mean_temp = mean_temp_min(df)
    mean_temp_accuracy_name, mean_temp_accuracy_sub = mean_data(df, name_mean_temp_min)
    name_mean_min_temp_accuracy, sub_mean_min_temp_accuracy = mean_temp_accuracy_min(mean_temp_accuracy_name,
                                                                                     mean_temp_accuracy_sub)
    name_mean_temp_max, round_mean_temp_max = mean_temp_max(mean_temp)
    mean_temp_accuracy_name, mean_temp_accuracy_sub = mean_data(df, name_mean_temp_max)
    name_mean_max_temp_accuracy, sub_mean_max_temp_accuracy = mean_temp_accuracy_max(mean_temp_accuracy_name,
                                                                                     mean_temp_accuracy_sub)
    name_mean_wind, round_mean_wind_max = mean_wind(df)

    return [name_mean_temp_min, round_mean_temp_min,
            name_mean_min_temp_accuracy, sub_mean_min_temp_accuracy,
            name_mean_temp_max, round_mean_temp_max,
            name_mean_max_temp_accuracy, sub_mean_max_temp_accuracy,
            name_mean_wind, round_mean_wind_max]

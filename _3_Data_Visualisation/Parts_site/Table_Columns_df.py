import pandas as pd


def name_df(df1: pd.DataFrame):
    table_columns = ["Айди", "Дата", "Название_г", "Долгота", "Широта", "Описание_осад",
                     "Темп", "Темп_макс(Вокруг_г/обл)", "Темп_мин(Вокруг_г/обл)", "Скор_ветра", "Гориз_ветра"]
    df1.columns = table_columns
    return df1

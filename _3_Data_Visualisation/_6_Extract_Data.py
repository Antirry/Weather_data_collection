import sys
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

import pymongo
from _4_To_run_programs.config import hostname
import datetime


def connect_db():
    try:
        client = pymongo.MongoClient(hostname, 27017)
        db = client['CitiesWeather_db']
        collections_1 = db.list_collection_names()

        # Это нужно для правильного порядка названий (База за: ) и (День/Месяц/Год)
        collections_2 = [collection_1[:9] for collection_1 in collections_1]
        collections_date = [collection_1[9:] for collection_1 in collections_1]
        # Лямбда находит все даты из названий дает возможность сортировки
        collections_date.sort(key=lambda date: datetime.datetime.strptime(date, "%d/%m/%Y"))

        collections_sort = list()

        for i in range(len(collections_1)):
            collections_sort.append(collections_2[i] + collections_date[i])

        return [db, collections_sort, collections_date]

    except Exception as ex:
        print("Проблема с базой, не может подключиться, ошибка в '_6_Extract_Data.py' ->", ex)
        return False


def wind_direction(value: int, wind_deg: float):
    wind_direction_ = {'Север': (348.75, 11.25), 'CевСевВосток': (11.25, 33.75), 'СевВосток': (33.75, 56.25),
                       'ВосСевВосток': (56.25, 78.75), 'Восток': (78.75, 101.25), 'ВосЮгоВосток': (101.25, 123.75),
                       'ЮгоВосток': (123.75, 146.25), 'ЮгоЮгоВосток': (146.25, 168.75), 'Юг': (168.75, 191.25),
                       'ЮгоЮгоЗапад': (191.25, 213.75), 'ЮгоЗапад': (213.75, 236.25), 'ЗапЮгоЗапад': (236.25, 258.75),
                       'Запад': (258.75, 281.25), 'ЗапСевЗап': (281.25, 303.75), 'СевЗапад': (303.75, 326.25),
                       'СевСевЗапад': (326.25, 348.75)}

    for key, value_list in wind_direction_.items():
        if value_list[0] < value < value_list[1]:
            return key
        elif 0 <= value < 11.25 or 348.75 < value <= 360:
            if wind_deg != 0.00:
                return 'Ceвер'
            else:
                return 'Нет ветра'


def check_coordination(update_dict: list, init: dict, i, i_0: int, date: list[str]):
    if 'longitude' in init and 'latitude' in init:
        update_dict.append({**{'_id': int(i), 'date': str(date[i_0])},
                            **{'name': str(init['name']),
                               "longitude": float(init['longitude']),
                               "latitude": float(init['latitude']),
                               'weather_disc': str(init['weather_disc']),
                               'temp': float(init['temp']),
                               'temp_max': float(init['temp_max']),
                               'temp_min': float(init['temp_min']),
                               'wind': float(init['wind']),
                               'wind_dir': wind_direction(int(init['wind_deg']), float(init['wind']))}})
    else:
        update_dict.append({**{'_id': int(i), 'date': str(date[i_0])},
                            **{'name': str(init['name']),
                               "longitude": float(-1),
                               "latitude": float(-1),
                               'weather_disc': str(init['weather_disc']),
                               'temp': float(init['temp']),
                               'temp_max': float(init['temp_max']),
                               'temp_min': float(init['temp_min']),
                               'wind': float(init['wind']),
                               'wind_dir': wind_direction(int(init['wind_deg']), float(init['wind']))}})


def retrieve_documents(connect_db_: list):
    data = list()
    for collection_1 in connect_db_[1]:
        col = connect_db_[0][collection_1]
        cursor = col.find()
        mongo_list_documents = list(cursor)

        data.append(mongo_list_documents)

    # Лямбда находит все айди из каждой таблицы базы данных и дает возможность сортировки
    new_list = [sorted(i, key=lambda _id: _id['_id']) for i in data]
    new_list = [doc for collection in new_list for doc in collection]

    update_dict = list()
    date = connect_db_[2]
    i_0 = 0

    for i, init in enumerate(new_list):
        if i != 0 and i % 50 == 0:
            i_0 += 1
        check_coordination(update_dict, init, i, i_0, date)

    """
    ПРОВЕРКА НА ДАТЫ
    update_data = {next(date): new_list[data_index-50:data_index] for data_index in range(50, len(new_list)+50, 50)}
    """
    return update_dict


def start_retrieve_documents() -> dict[str:list]:
    return retrieve_documents(connect_db())


"""
print(start_retrieve_documents())
"""
import pymongo
from To_run_programs_4.config import hostname
import datetime
from Data_generation_2.Call_API_3 import cities_list_weather


def connect_db():
    try:
        client = pymongo.MongoClient(hostname, 27017)
        db = client['CitiesWeather_db']
        name = datetime.datetime.now().strftime("%d/%m/%Y")
        collection = db["База за: " + name]
        return collection

    except Exception as ex:
        print("Проблема с базой, не может подключиться, ошибка в 'Write_in_DB_4.py' ->", ex)
        return False


def write_db():
    try:
        collection = connect_db()
        cities_list_dict_weather = cities_list_weather()
        collection.insert_many(cities_list_dict_weather)

    except Exception as ex:
        print("Такая база уже есть, ошибка в 'Write_in_DB_4.py' ->", ex)
        return False

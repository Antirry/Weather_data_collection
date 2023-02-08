import pymongo
from _4_To_run_programs.config import hostname
import datetime
from _2_Data_generation._3_Call_API import start_cities_list_weather


def connect_db():
    try:
        client = pymongo.MongoClient(hostname, 27017)
        db = client['CitiesWeather_db']
        name = datetime.datetime.now().strftime("%d/%m/%Y")
        collection = db["База за: " + name]
        return collection

    except Exception as ex:
        print("Проблема с базой, не может подключиться, ошибка в '_4_Write_in_DB.py' ->", ex)
        return False


def write_db():
    try:
        collection = connect_db()
        cities_list_dict_weather = start_cities_list_weather()
        print("\n", "Запись в базу...")
        collection.insert_many(cities_list_dict_weather)

    except Exception as ex:
        print("Такая база уже есть, ошибка в '_4_Write_in_DB.py' ->", ex)
        return False

import pymongo
from config import hostname
import datetime
from Call_API_3 import cities_list_weather
try:
    client = pymongo.MongoClient(hostname, 27017)
    db = client['CitiesWeather_db']
    name = datetime.datetime.now().strftime("%d/%m/%Y")
    collection = db["База за: " + name]
except Exception as ex:
    print("Проблема с базой, не может подключиться, ошибка в 'Write_in_DB_4.py' ->", ex)


def write_db():
    try:
        cities_list_dict_weather = cities_list_weather()
        collection.insert_many(cities_list_dict_weather)
    except Exception as ex:
        print("Такая база уже есть, ошибка в 'Write_in_DB_4.py' ->", ex)
        return False

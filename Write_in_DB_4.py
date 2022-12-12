import pymongo
from config import hostname
import datetime
from Call_API_3 import cities_list_weather

client = pymongo.MongoClient(hostname, 27017)
db = client['CitiesWeather_db']
name = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
collection = db["База за: " + name]

cities_list_dict_weather = cities_list_weather()
collection.insert_many(cities_list_dict_weather)

print("\n БАЗА ГОТОВА \n")

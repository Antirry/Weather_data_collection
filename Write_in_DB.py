import pymongo
from config import hostname
from Call_API import cities_list_weather
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


async def aggregate():
    # try:
    """
    ОШИБКА = AttributeError: 'str' object has no attribute 'insert_many'
    """
    db = client.CitiesWeather_db
    collection = db.name
    cities_list_dict_weather = cities_list_weather()
    results = await collection.insert_many(cities_list_dict_weather)
    """
    Второй вариант (Не рабочий)
    
    db = client.get_database('CitiesWeather_db')
    collection = db.get_collection('name')
    cities_list_dict_weather = cities_list_weather()
    cursor = collection.aggregate(pipeline=cities_list_dict_weather)
    results = await cursor.to_list(length=1000)
    return results
    """
    return results
    # except Exception as ex:
    #     print(f"Ошибка {ex}")

client = AsyncIOMotorClient("citiesweather.bojdf46.mongodb.net", 27017)
asyncio.get_event_loop().run_until_complete(aggregate())

"""
f"mongodb+srv://{admin_user}:{admin_password}@citiesweather.bojdf46.mongodb.net"
                            f"/?retryWrites=true&w=majority"
"""
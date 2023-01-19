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


def retrieve_documents():
    data = list()
    connect_db_ = connect_db()
    for collection_1 in connect_db_[1]:
        col = connect_db_[0][collection_1]
        cursor = col.find()
        mongo_list_documents = list(cursor)

        data.append(mongo_list_documents)

    # Лямбда находит все айди из каждой таблицы базы данных и дает возможность сортировки
    new_list = [sorted(i, key=lambda _id: _id['_id']) for i in data]
    new_list = [doc for collect in new_list for doc in collect]

    return [new_list, connect_db_[2]]



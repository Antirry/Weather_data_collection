import requests
from pprint import pprint
from config import open_weather_token
from Read_xlsx import read_xlsx as cities


def get_weather(city_name, open_weather_token):
    try:
        lang = "ru"
        units = "metric"
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={open_weather_token}&units={units}&lang={lang}"
        )
        data = req.json()
        pprint(data)
    except Exception as ex:
        print(f"Ошибка - {ex}")


def main():
    try:
        get_weather('Москва', open_weather_token)
    except OSError:
        print("Не в том месте вывод, стоит посмотреть '.txt' файл")


main()
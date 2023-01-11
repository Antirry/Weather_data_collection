import requests
import datetime
from To_run_programs_4.config import open_weather_token
from Rosstat_xlsx_1.Read_xlsx_2 import read_xlsx as cities


def get_weather(city_name, open_weather_token) -> (dict[str, int, float], bool):
    try:
        lang = "ru"
        units = "metric"
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={open_weather_token}&units={units}&lang={lang}"
        )
        data = req.json()

        name = data['name']
        date_time = datetime.datetime.utcfromtimestamp(data["dt"]).strftime('%d-%m-%Y %H:%M:%S')
        date_time = datetime.datetime.strptime(date_time, '%d-%m-%Y %H:%M:%S')
        weather_disc = data['weather'][0]['description']
        temp = data['main']['temp']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        wind = data['wind']['speed']
        wind_deg = data['wind']['deg']

        weather_dict = {
            "name": str(name),
            "date_time": date_time,
            "weather_disc": str(weather_disc),
            "temp": temp,
            "temp_max": temp_max,
            "temp_min": temp_min,
            "wind": wind,
            "wind_deg": wind_deg
        }

        return weather_dict

    except Exception as ex:
        print(f"Ошибка в создании словаря")
        print(f"Ошибка в 'Call_API_3.py' - {ex}")
        return False


def cities_list_weather() -> list[dict[str, int, float]]:
    list_weathers = list()
    cities_list = cities()
    i = 1
    for city in cities_list:
        weather_city = dict({'_id': i}, **get_weather(city, open_weather_token))
        list_weathers.append(weather_city)
        print(city, "\n Обработан запрос из списка")
        i += 1

    return list_weathers


"""
print(cities_list_weather())

print("\n Имя города -> name",
      "\n Время данных -> date_time",
      "\n Описание погоды -> weather",
      "\n Температура (по цельсию) temp",
      "\n Температура в пределах крупных мегаполисов и городских территорий: "
      "\n      максимальная (по цельсию) -> temp_max",
      "\n      минимальная (по цельсию) -> temp_min",
      "\n Скорость ветра (м/c)-> wind",
      "\n Направление ветра (градусы) -> wind_deg")

Нужно сделать запрос в бд:

  1: который будет предупреждать о максимальной высокой/низкой температуре, 
  так как из-за этого может случится ЧП;
  
  2: который будет предупреждать о аномальных осадках;
"""

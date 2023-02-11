import requests
from _4_To_run_programs.config import open_weather_token
from _1_Rosstat_xlsx._2_Read_xlsx import read_xlsx as cities


def get_weather(city_name, open_weather_token) -> (dict[str, int, float], bool):
    try:
        lang = "ru"
        units = "metric"
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={open_weather_token}&units={units}&lang={lang}"
        )
        data = req.json()

        name = data['name']
        longitude = data['coord']['lon']
        latitude = data['coord']['lat']
        weather_disc = data['weather'][0]['description']
        temp = data['main']['temp']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        wind = data['wind']['speed']
        wind_deg = data['wind']['deg']

        weather_dict = {
            "name": str(name),
            "longitude": longitude,
            "latitude": latitude,
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


def cities_list_weather(cities_list) -> list[dict[str, int, float]]:
    list_weathers = list()
    i = 1
    for city in cities_list:
        weather_city = dict({'_id': i}, **get_weather(city, open_weather_token))
        list_weathers.append(weather_city)
        print(city, "\n Обработан запрос из списка")
        i += 1

    return list_weathers


def start_cities_list_weather():
    return cities_list_weather(cities())


"""
print(cities_list_weather())

print("\n Имя города -> name",
      "\n Геолокация города: "
      "\n      долгота -> longitude",
      "\n      широта -> latitude",
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

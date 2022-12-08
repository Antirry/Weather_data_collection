import requests
import datetime
from config import open_weather_token
from Read_xlsx import read_xlsx as cities


def get_weather(city_name, open_weather_token):
    try:
        weather_list = list()
        lang = "ru"
        units = "metric"
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={open_weather_token}&units={units}&lang={lang}"
        )
        data = req.json()

        name = data['name']
        date_time = datetime.datetime.fromtimestamp(data['dt'])
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        wind = data['wind']['speed']
        wind_deg = data['wind']['deg']

        weather_list.extend((name, str(date_time), weather, temp, temp_max, temp_min, wind, wind_deg))
        return weather_list

    except Exception as ex:
        print(f"Ошибка - {ex}")


def cities_list_weather() -> list[list[any]]:
    list_weathers = list()
    list_weathers.append((get_weather("Москва", open_weather_token)))
    print("Обработан запрос из списка")

    # for city in cities():
    #     list_weathers.append(get_weather(city, open_weather_token))

    return list_weathers


"""
print(cities_list_weather())

print("\n Имя города -> ", name,
      "\n Время данных -> ", date_time,
      "\n Описание погоды -> ", weather,
      "\n Температура (по цельсию) -> ", temp,
      "\n Температура в пределах крупных мегаполисов и городских территорий: "
      "\n      максимальная (по цельсию) -> ", temp_max,
      "\n      минимальная (по цельсию) -> ", temp_min,
      "\n Скорость ветра (м/c)-> ", wind,
      "\n Направление ветра (градусы) -> ", wind_deg)

Нужно сделать запрос в бд:

  1: который будет предупреждать о максимальной высокой/низкой температуре, 
  так как из-за этого может случится ЧП;
  
  2: который будет предупреждать о аномальных осадках;
"""

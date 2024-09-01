# добавляем модуль для работы с JSON-форматом
import json
# добавляем модуль для HTTP-запросов
import urllib.request
# добавляем модуль рисования
import turtle
# модуль для использования возможностей операционной системы
import os
# добавляем модуль для работы со временем
import time
# добавляем модуль для открытия URL-адресов по умолчанию
import webbrowser
# импортируем типы данных для аннотации типов
from typing import Dict, List, Any
from http.client import HTTPResponse


def main():
    # задаём адрес для запроса списка космонавтов
    url: str = 'http://api.open-notify.org/astros.json'
    # открываем URL, используя urllib.request
    res: HTTPResponse = urllib.request.urlopen(url)
    # загружаем и читаем json-файл
    result: Dict[str, Any] = json.loads(res.read())
    # создаём текстовый файл с именами членов экипажа

    # открываем файл для записи
    with open('iss.txt', 'w') as file:
        # добавляем запись
        file.write(f'В настоящий момент на МКС {str(result["number"])} астронавтов:\n\n')
        # получаем список имён космонавтов
        people: List[Dict[str, str]] = result['people']
        # для каждого человека в списке выводим его имя
        for person in people:
            file.write(person['name'] + '\n')

    # получаем абсолютный путь к файлу
    file_path: str = os.path.abspath('iss.txt')
    # открываем файл в отдельном окне
    webbrowser.open(f'file://{file_path}')

    # устанавливем карту мира
    screen: turtle.Screen = turtle.Screen()
    # устанавливаем размеры окна
    screen.setup(1280, 720)
    # устанавливаем систему координат для экрана, аналогичную с координатами Земли
    screen.setworldcoordinates(-180, -90, 180, 90)

    # загружааем изображение карты мира из файла
    screen.bgpic('map.gif')
    # загружаем изображение станции из файла
    screen.register_shape('iss.gif')
    # присваиваем переменной iss значение объекта Turtle
    iss = turtle.Turtle()
    # придаём переменной вид изображения станции из файла
    iss.shape('iss.gif')
    # выключаем функцию рисование следа от объекта Turtle()
    iss.penup()

    # запускаем бесконечный цикл
    while True:
        # прописываес адрес для запроса о текущем положении МКС
        url: str = 'http://api.open-notify.org/iss-now.json'
        # объявляем переменную и сохраняем в неё ответ
        res: HTTPResponse = urllib.request.urlopen(url)
        # переводим ответ в JSON и читаем
        result: Dict[str, Dict[str, str]] = json.loads(res.read())

        # извлекаем локацию станции
        location: Dict[str, str] = result['iss_position']
        # извлекаем только широту станции
        lat: float = float(location['latitude'])
        # извлекаем только долготу станции
        lon: float = float(location['longitude'])

        # Получение текущего времени
        current_time: str = time.strftime("%Y-%m-%d %H:%M:%S")
        # Вывод на экран
        print("\nДата и время:", current_time)
        # переводим широту и долготу в числа с плавающей запятой
        lat = float(lat)
        lon = float(lon)
        # выводим широту и долготу в терминал
        print(f'Широта: {str(lat)}')
        print(f'Долгота: {str(lon)}')

        # обновляем локация станции на карте
        iss.goto(lon, lat)

        # обновляем каждые 5 секунд
        time.sleep(5)


# запускаем программу
main()

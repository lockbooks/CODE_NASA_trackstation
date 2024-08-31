# добавляем модуль для работы с JSON-форматом
import json
# добавляем модуль рисования
import turtle
# добавляем модуль для HTTP-запросов
import urllib.request
# добавляем модуль для работы со временем
import time
# добавляем модуль для открытия URL-адресов по умолчанию
import webbrowser
# добавляем модуль геокодирования и перевода адресов в координаты
import geocoder
# модуль для использования возможностей операционной системы
import os


def main():
    # Free API
    url = 'http://api.open-notify.org/astros.json'
    # открываем URL, используя urllib.request
    res = urllib.request.urlopen(url)
    # загружаем и читаем json-файл
    result = json.loads(res.read())
    # создаём текстовый файл с именами членов экипажа
    file = open('iss.txt', 'w')
    file.write(f'В настоящий момент на ISS {str(result["number"])} астронавтов \n\n')
    people = result['people']
    for person in people:
        file.write(person['name'] + ' на борту' + '\n')

    g = geocoder.ipinfo()
    file.write(f'\nВаши текущие широта и долгота: {str(g.latlng)}')
    file.close()

    # получаем абсолютный путь к файлу
    file_path = os.path.abspath('iss.txt')
    # открываем файл браузером
    # это будет выглядеть как обычный текстовый файл
    webbrowser.open(f'file://{file_path}')

    # устанавливем карту мира
    screen = turtle.Screen()
    screen.setup(1280, 720)
    screen.setworldcoordinates(-180, -90, 180, 90)

    # загружааем изображение карты мира
    screen.bgpic('map.gif')
    screen.register_shape('iss.gif')
    iss = turtle.Turtle()
    iss.shape('iss.gif')
    iss.setheading(45)
    iss.penup()

    while True:
        # загружаем текущий статус ISS в реальном времени
        url = 'http://api.open-notify.org/iss-now.json'
        res = urllib.request.urlopen(url)
        result = json.loads(res.read())

        # извлекаем локацию станции
        location = result['iss_position']
        lat = location['latitude']
        lon = location['longitude']

        # выводим широту и долготу в терминал
        lat = float(lat)
        lon = float(lon)
        print(f'\nШирота: {str(lat)}')
        print(f'\nДолгота: {str(lon)}')

        # обновляем локация станции на карте
        iss.goto(lon, lat)

        # обновляем каждые 5 секунд
        time.sleep(5)


main()

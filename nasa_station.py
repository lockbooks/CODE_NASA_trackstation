import json
import turtle
import urllib.request
import time
import webbrowser
import geocoder


def main():
    # Free API
    url = 'http://api.open-notify.org/astros.json'
    # открываем URL, используя urllib.request
    res = urllib.request.urlopen(url)
    # загружаем и читаум json-файл
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

    webbrowser.open('iss.txt')

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

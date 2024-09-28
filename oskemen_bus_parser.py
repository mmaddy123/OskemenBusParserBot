from selenium import webdriver
from bs4 import BeautifulSoup
from collections import namedtuple


IncomingBus = namedtuple('IncomingBus',
                         ['bus_stop_name', 'bus_route', 'first_incoming_time', 'second_incoming_time'])


# Temporary
def get_bus_stop_names():
    return {"Пр.Сатпаева": 304129, "ВКГТУ": 173057}


def get_bus_stop_by_url(stop):
    bus_stop_code = get_bus_stop_names()
    url = f"https://oskemenbus.kz/maps?z=11&lat=49.95718404030751&lng=82.59109497070314&mode=3" \
          f"&stop={bus_stop_code[stop]}"
    return url


def get_bus_stop_html(bus_stop_url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    browser = webdriver.Chrome(options=options)
    browser.get(bus_stop_url)

    soup = BeautifulSoup(browser.page_source, features="html.parser")

    bus_stop_routes_html = soup.find_all("div", {"class": "ng-star-inserted"})

    # bus_stop_name = soup.find("p", {"class": "stop-info__stop-name"}).text
    # print(bus_stop_name)

    return bus_stop_routes_html


def get_incoming_bus(bus_route, bus_stop_routes_html, bus_stop_name):
    incoming_bus = None
    for bus_route_data in bus_stop_routes_html:
        try:
            bus_number = bus_route_data.find_next("app-scoreboard-note", {"class": "ng-star-inserted"}) \
                .find("p", {"class": "info-row__vehicle-number"}).text
            first_incoming_time = bus_route_data.find_next("app-scoreboard-note", {"class": "ng-star-inserted"}) \
                .find("p", {"class": "info-row__first-time ng-star-inserted"}).text.strip()
            second_incoming_time = bus_route_data.find_next("app-scoreboard-note", {"class": "ng-star-inserted"}) \
                .find("p", {"class": "info-row__second-time ng-star-inserted"}).text.strip()
            if bus_number == bus_route:
                incoming_bus = IncomingBus(bus_stop_name, bus_route, first_incoming_time, second_incoming_time)
        except AttributeError as e:
            print("Автобусы на данный момент не ходят")
    return incoming_bus


def get_bus_routes(bus_stop_routes_html):
    bus_routes = []
    for bus_route_data in bus_stop_routes_html:
        bus_number = bus_route_data.find_next("app-scoreboard-note", {"class": "ng-star-inserted"}) \
            .find("p", {"class": "info-row__vehicle-number"}).text
        if bus_number not in bus_routes:
            bus_routes.append(bus_number)
    return bus_routes

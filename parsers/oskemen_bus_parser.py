import requests
import json
import ndjson
from collections import namedtuple
from enum import Enum

IncomingBus = namedtuple('IncomingBus',
                         ['first_incoming_time', 'second_incoming_time', 'longitude', 'latitude'])


def get_bus_stop_names():
    # return {304129: "Пр.Сатпаева", 173057: "ВКГТУ", 171009: "Ровесник"}
    return {"Сатпаева": 304129,
            "ВКТУ": 173057,
            "Ровесник": 171009,
            'Ивушка': 458753,
            "Колос": 71681,
            "Есенберлина": 478209,
            "Речной вокзал": 186369,
            "Дворец": 47105}


class OskemenBusParser:
    def __init__(self):
        self.bus_stop_name = None
        self.bus_route = None
        self.bus_route_id = None
        self.first_incoming_bus_id = None

    def get_bus_stop_json(self):
        bus_stop_api_url = "https://oskemenbus.kz/api/GetScoreboard"
        stop_id = get_bus_stop_names()[self.bus_stop_name]
        payload = {'StopId': stop_id, 'Types': None}
        response = requests.post(url=bus_stop_api_url, data=json.dumps(payload))
        if response.status_code == 200:
            bus_stop_data = response.json(cls=ndjson.Decoder)
            return bus_stop_data

    @staticmethod
    def format_incoming_time(minutes):
        result = []
        if minutes is None:
            result.append("-")
        else:
            hour = minutes // 60
            if hour > 0:
                result.append(f"{hour}ч")
            if -2 <= minutes <= 0:
                result.append(f"Прибывает")
            else:
                minutes = minutes % 60
                result.append(f"{minutes}мин")

        return " ".join(result)

    def get_bus_routes(self):
        bus_routes = []
        if self.get_bus_stop_json() is not None:
            for data in self.get_bus_stop_json():
                bus_routes.append(data["result"]["Number"])
        return bus_routes

    def get_incoming_bus(self):
        incoming_bus = None
        if self.get_bus_stop_json() is not None:
            for data in self.get_bus_stop_json():
                if data['result']['Number'] == self.bus_route:
                    self.first_incoming_bus_id = data['result']['IdVehicle1']
                    self.bus_route_id = data['result']['RouteId']
                    latitude, longitude = self.get_bus_location()
                    first_incoming_time = self.format_incoming_time(data['result']['InfoM'][0])
                    second_incoming_time = self.format_incoming_time(data['result']['InfoM'][1])
                    incoming_bus = IncomingBus(first_incoming_time, second_incoming_time,
                                               latitude, longitude)
        return incoming_bus

    def get_bus_location(self):
        bus_data_api_url = "https://oskemenbus.kz/api/GetRouteVehicles"
        bus_id = self.first_incoming_bus_id
        route_id = self.bus_route_id
        payload = {'RouteId': route_id}
        response = requests.post(url=bus_data_api_url, data=json.dumps(payload))
        latitude = None
        longitude = None
        if response.status_code == 200:
            route_buses_data = response.json(cls=ndjson.Decoder)
            for data in route_buses_data[0]['Vehicles']:
                if data['VehicleId'] == str(bus_id):
                    latitude = data['Point']['Latitude']
                    longitude = data['Point']['Longitude']
        return latitude, longitude

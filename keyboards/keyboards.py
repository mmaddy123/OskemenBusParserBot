from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup,\
    InlineKeyboardButton, ReplyKeyboardRemove, KeyboardButton
import math


def create_bus_routes_buttons(bus_routes):
    if bus_routes is None:
        return None
    else:
        rows = math.ceil(len(bus_routes) / 3)
        routes_keyboard = [[] for i in range(rows)]
        for i in range(len(bus_routes)):
            routes_keyboard[i // 3].append(KeyboardButton(text=bus_routes[i]))
        keyboards = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=routes_keyboard)
        return keyboards

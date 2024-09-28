from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup,\
    InlineKeyboardButton, ReplyKeyboardRemove, KeyboardButton
import math


def create_bus_routes_buttons(bus_routes):
    rows = math.ceil(len(bus_routes) / 3)
    routes_keyboard = [[] for i in range(rows)]
    for i in range(len(bus_routes)):
        routes_keyboard[i // 3].append(KeyboardButton(text=bus_routes[i]))
    keyboards = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=routes_keyboard)
    return keyboards


# def create_bus_routes_buttons(bus_routes):
#     # Создаем клавиатуру с возможностью изменения размера
#     keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
#
#     # Определяем количество строк
#     rows = math.ceil(len(bus_routes) / 3)
#
#     # Проходим по всем маршрутам
#     for i in range(rows):
#         # Добавляем кнопки по 3 в ряд
#         buttons = [KeyboardButton(text=bus_routes[j]) for j in range(i * 3, min((i + 1) * 3, len(bus_routes)))]
#          # Добавляем сразу несколько кнопок на одну строку
#
#     return keyboard

# create_bus_routes_buttons(["60", "33", "46", "26", "46a", "26a", "17"])

# routes_keyboard_temporary = [[
#     KeyboardButton(text="60"),
#     KeyboardButton(text="33"),
#     KeyboardButton(text="17"),
# ]]


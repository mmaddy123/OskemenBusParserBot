"""Для просмотра списка доступных автобусных остановок с направлениями маршрута"""
import os
from aiogram import types, Router, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from bot import dp, bot
from states import SelectBusStop
from oskemen_bus_parser import get_incoming_bus, get_bus_stop_names, get_bus_routes


router = Router()


@router.message(Command("get_bus_stops"))
async def get_available_buses(message: types.Message):
    await message.answer("Пока есть только остановки Пр.Сатпаева и ВКГТУ")

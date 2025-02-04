from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from parsers import OskemenBusParser


class BusParserMiddleWare(BaseMiddleware):
    def __init__(self, bus_parser: OskemenBusParser):
        self.bus_parser = bus_parser

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        data['bus_parser'] = self.bus_parser
        result = await handler(event, data)
        return result

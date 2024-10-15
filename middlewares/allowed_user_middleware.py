import os
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class AllowedUsersMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]):
        user = data["event_from_user"]
        if user.id in list(map(int, (os.getenv("USERS_ID").split(",")))):
            return await handler(event, data)
        else:
            return

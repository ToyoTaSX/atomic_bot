import asyncio
import logging
import sys
from os import getenv
from pprint import pprint

from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session import aiohttp
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F
from aiogram.types import Message, InputMediaPhoto, InputMedia, ContentType as CT
import asyncio
from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message


class AlbumMiddleware(BaseMiddleware):
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        self.latency = latency

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: dict[str, Any]
    ) -> Any:
        if not message.media_group_id:
            data['album'] = [message]
            await handler(message, data)
            return
        try:
            self.album_data[message.media_group_id].append(message)
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            data['_is_last'] = True
            data["album"] = self.album_data[message.media_group_id]
            await handler(message, data)

        if message.media_group_id and data.get("_is_last"):
            del self.album_data[message.media_group_id]


# class AlbumMiddleware(BaseMiddleware):
#     def __init__(self, latency: Union[int, float] = 0.01):
#         self.latency = latency
#         self.album_data = {}
#
#     async def __call__(
#             self,
#             handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
#             message: Message,
#             data: dict[str, Any]
#     ) -> Any:
#         if not message.media_group_id:
#             data['album'] = [message]
#             await handler(message, data)
#             return
#
#         if message.media_group_id not in self.album_data:
#             self.album_data[message.media_group_id] = []
#
#         self.album_data[message.media_group_id].append(message)
#
#         await asyncio.sleep(self.latency)
#
#         if len(self.album_data[message.media_group_id]) > 1:
#             data['album'] = self.album_data.pop(message.media_group_id, [])
#             await handler(message, data)
#         else:
#             data['album'] = [message]
#             await handler(message, data)
#
#         if message.media_group_id in self.album_data:
#             del self.album_data[message.media_group_id]
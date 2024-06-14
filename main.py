import asyncio
import logging
import os
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
from aiogram.types import Message, InputMediaPhoto, InputMedia, FSInputFile, ContentType as CT


from model_requests import get_weld_photo_class
from bot_middlewares import AlbumMiddleware
import asyncio
from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message


TOKEN = '7278125173:AAH34aKuLGN1yBwDw11KIVmSAFaZH7aPK2Y'
dp = Dispatcher()
bot = Bot(token=TOKEN)
dp.message.middleware(AlbumMiddleware())


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Приветствую, отправь мне фото сварочного шва, и я определю наличие дефектов")


@dp.message(F.content_type.in_([CT.PHOTO, CT.VIDEO, CT.AUDIO, CT.DOCUMENT]))
async def handle_albums(message: Message, album: list[Message]):
    photos_id = []
    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            photos_id.append(file_id)
        else:
            obj_dict = msg.dict()
            file_id = obj_dict[msg.content_type]['file_id']
            photos_id.append(file_id)
    photos = await download_photos(photos_id, root='users_photos')
    for photo in photos:
        weld_class = await get_weld_photo_class(photo)
        await message.answer_photo(FSInputFile(path=photo), caption=weld_class)
        os.remove(photo)

async def download_photos(photos_ids, root):
    photos_pathes = []
    for photo_id in photos_ids:
        file = await bot.get_file(photo_id)
        dest = f'{root}/photo_{photo_id}.png'
        await bot.download_file(file_path=file.file_path, destination=dest)
        photos_pathes.append(dest)
    return photos_pathes


async def main() -> None:
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
import logging
import asyncio
import logging
import os
import sys
import uuid

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, ContentType as CT
from aiogram.types import Message, BufferedInputFile

from bot_middlewares import AlbumMiddleware
from model_requests import find_defects_on_photo
from config import TOKEN

dp = Dispatcher()
bot = Bot(token=TOKEN, timeout=30)
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
    await message.answer('Подождите немного, идет загрузка')
    for photo in photos:
        processed_photo_bytes = await find_defects_on_photo(photo)
        await message.answer_photo(BufferedInputFile(file=processed_photo_bytes, filename='photo'))
        print(photo)
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
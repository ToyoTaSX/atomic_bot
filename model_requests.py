from pprint import pprint

import requests
import base64
from config import API_URL


async def find_defects_on_photo(photo_path):
    try:
        with open(photo_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(API_URL, files=files)
            if response.ok:
                image64 = response.json().get('image_base64')
                image_data = base64.b64decode(image64)
                return image_data
            return 'Ошибка сервера'
    except Exception as e:
        return str(e)

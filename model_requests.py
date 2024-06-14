from pprint import pprint

import requests

api_url = 'http://127.0.0.1:8000/api/get_photo_class/'


async def get_weld_photo_class(photo_path):
    try:
        with open(photo_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(api_url, files=files)
            if response.ok:
                return response.json().get('class')
            return 'Ошибка сервера'
    except Exception as e:
        return str(e)

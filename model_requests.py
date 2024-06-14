import random


async def get_weld_photo_class(photo):
    print(photo)
    classes = ['Идеальный шов', 'Непроваренный шов', 'Трещина']
    return random.choice(classes)
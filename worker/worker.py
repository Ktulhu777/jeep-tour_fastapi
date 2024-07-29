from io import BytesIO

from celery import Celery
from PIL import Image
from config.config import REDIS_HOST, REDIS_PORT

celery = Celery('worker',
                broker=f'redis://{REDIS_HOST}:{REDIS_PORT}',
                backend=f'redis://{REDIS_HOST}:{REDIS_PORT}',
                broker_connection_retry_on_startup=True)

@celery.task
def image(photo_data: bytes, filename: str):
    with BytesIO(photo_data) as img_file:
        with Image.open(img_file) as img:
            img = img.convert('RGB')
            img.save(filename)
    return filename

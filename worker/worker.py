from celery import Celery
from PIL import Image
from config.config import REDIS_HOST, REDIS_PORT

celery = Celery('worker', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}', backend='redis://')
celery.broker_connection_retry_on_startup = True


@celery.task
def image(username: str, filepath: str):
    filename = f'ava_{username}.png'
    with Image.open(filepath) as img:
        img = img.convert('RGB')
        img.save(filename)
        img.close()
    return filename

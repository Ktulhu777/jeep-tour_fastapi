#  сторонние библиотеки
import aioredis
from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
# мои модули
from oauth.oauth import router as oauth
from home_page.home import router as attraction
from config.config import REDIS_HOST, REDIS_PORT

app = FastAPI(title="Jeep tour")
app.include_router(router=attraction)
app.include_router(router=oauth, prefix="/user")

origins = [
    "http://localhost:8001",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Список разрешенных источников
    allow_credentials=True,  # Разрешить отправку cookie и других данных авторизации
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PUT", "PATCH"],  # Разрешенные методы
    allow_headers=["*"],  # Разрешенные заголовки
)


@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}', encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis=redis), prefix='fastapi-cache')


if __name__ == '__main__':
    uvicorn.run('app:app', host="0.0.0.0", port=5000, reload=True)

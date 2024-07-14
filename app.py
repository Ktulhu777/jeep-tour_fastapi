#  сторонние библиотеки #
from fastapi import FastAPI
import uvicorn

# мои модули #
from oauth.oauth import router as oauth

app = FastAPI(title="Jeep tour")
app.include_router(router=oauth, prefix="/user")


@app.get("/")
def index_home():
    return "Главная страница"


if __name__ == '__main__':
    uvicorn.run('app:app', host="0.0.0.0", port=5000, reload=True)

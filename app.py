#  сторонние библиотеки #
from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

# мои модули #
from oauth.oauth import router as oauth

app = FastAPI(title="Jeep tour")
app.include_router(router=oauth, prefix="/user")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index_home():
    return "Главная страница"


if __name__ == '__main__':
    uvicorn.run('app:app', host="0.0.0.0", port=5000, reload=True)

#  python API #
from typing import Annotated, Dict

#  сторонние библиотеки #
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

# мои модули #
from models.models import Users
from database_engine import get_async_session
from .hashing import Hasher
from .crud_database import get_user, add_user_in_database, exists_user_by_phone, change_password_db
from .schema import GetMeUser, RegisterUser, ChangePassword

router = APIRouter()
security = HTTPBasic()


async def basic_auth_validate(user: Annotated[HTTPBasicCredentials, Depends(security)],
                              session: AsyncSession = Depends(get_async_session)):
    user_with_db = await get_user(username=user.username, session=session)
    if not Hasher.verify_password(plain_password=user.password, hashed_password=user_with_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid username or password")
    return user_with_db


async def get_current_user(user: Annotated[HTTPBasicCredentials, Depends(security)],
                           session: AsyncSession = Depends(get_async_session)):
    """Функция получает авторизованного текущего пользователя"""
    return await get_user(username=user.username, session=session)


@router.post("/auth/", response_model=GetMeUser)
def basic_auth(user: Dict = Depends(basic_auth_validate)):
    """Функция происзводит авторизацию пользователя"""
    return user


@router.get("/me/profile/", response_model=GetMeUser)
def get_user_me(user: Users = Depends(get_current_user)):
    """Возвращает профиль пользователя"""
    return user


@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(user: Annotated[RegisterUser, Depends()],
                        session: AsyncSession = Depends(get_async_session)):
    """Регистрация пользователя на сайте"""
    hashed_password = Hasher.get_password_hash(user.password_1)
    await exists_user_by_phone(user.phone, session)
    await add_user_in_database(user.username, user.phone, hashed_password, session)
    return {"success": "Пользователь успешно зарегистрирован!"}


@router.post("/change-password/")
async def change_password(user: Annotated[HTTPBasicCredentials, Depends(security)],
                          password: Annotated[ChangePassword, Depends()],
                          session: AsyncSession = Depends(get_async_session)):
    """Функция смены пароля"""
    # Проверка паролей
    user_with_db = await get_user(user.username, session)
    if not Hasher.verify_password(
            plain_password=password.old_password,
            hashed_password=user_with_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Неверный старый пароль")
    # Обновление пароля
    new_hashed_password = Hasher.get_password_hash(password.password_1)
    await change_password_db(username=user_with_db.username,
                             new_hash_password=new_hashed_password,
                             session=session)
    return {"success": "Пароль изменен"}

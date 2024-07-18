#  python API #
from typing import Annotated, Dict, Optional
import os

#  сторонние библиотеки #
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

# мои модули #
from models.models import Users
from database_engine import get_async_session
from s3_client import s3client
from .hashing import Hasher
from .crud_database import get_user, add_user_in_database, exists_user_by_phone, change_password_db, delete_user_db
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


@router.put('/update/me/profile/')
async def update_auth_user(user: Annotated[HTTPBasicCredentials, Depends(security)],
                           session: AsyncSession = Depends(get_async_session)):
    """Функция не работает"""
    return "Функция заглушка"


@router.delete('/delete/me/profile/')
async def delete_auth_user(user: Annotated[HTTPBasicCredentials, Depends(security)],
                           session: AsyncSession = Depends(get_async_session)):
    """Удаление авторизованного пользователя"""
    await delete_user_db(username=user.username, session=session)
    s3client.remove_bucket(user.username)
    return {"success": "Пользователь успешно удален"}


@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(user: Annotated[RegisterUser, Depends()],
                        photo: UploadFile = File(...),
                        session: AsyncSession = Depends(get_async_session)):
    """Регистрация пользователя на сайте"""
    hashed_password = Hasher.get_password_hash(user.password_1)
    username = user.username
    await exists_user_by_phone(user.phone, session)
    await add_user_in_database(username, user.phone, hashed_password, session)
    s3client.make_bucket(username)
    if photo:
        file_size = os.fstat(photo.file.fileno()).st_size
        s3client.put_object(username, photo.filename, photo.file, file_size)
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

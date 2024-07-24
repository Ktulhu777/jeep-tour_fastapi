#  python API #
from typing import Annotated, Dict

#  сторонние библиотеки #
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession

# мои модули #
from models.models import Users
from database_engine import get_async_session
from s3_client import s3_client
from .hashing import Hasher
from .default_img import make_default_png
from .crud_database import get_user, add_user_in_database, exists_user_by_phone, change_password_db, delete_user_db
from .schema import GetMeUser, RegisterUser, ChangePassword

router = APIRouter()
security = HTTPBasic()


async def get_auth_user_and_session(
        user: Annotated[HTTPBasicCredentials, Depends(security)],
        session: AsyncSession = Depends(get_async_session)
) -> Dict:
    return {"user": user,
            "session": session}


async def basic_auth_validate(component: Dict = Depends(get_auth_user_and_session)):
    user_with_db = await get_user(username=component['user'].username, session=component['session'])
    if not Hasher.verify_password(plain_password=component['user'].password,
                                  hashed_password=user_with_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid username or password")
    return user_with_db


async def get_current_user(user: Users = Depends(basic_auth_validate)):
    """Функция получает авторизованного текущего пользователя"""
    return user


@router.post("/auth/", response_model=GetMeUser)
async def basic_auth(user: Users = Depends(basic_auth_validate)):
    """Функция производит авторизацию пользователя"""
    async with ClientSession() as session:
        photo = await s3_client.get_object(bucket_name=user.username,
                                           object_name=f'ava_{user.username}.png',
                                           session=session)

    return GetMeUser(id=user.id, username=user.username, phone=user.phone,
                     url=str(photo.url).replace('minio', 'localhost'),  # пока оставлю костыль
                     register_data=user.register_data, is_active=user.is_active, is_superuser=user.is_superuser,
                     is_verified=user.is_verified)


@router.get("/me/profile/", response_model=GetMeUser)
async def get_user_me(user: Users = Depends(get_current_user)):
    """Возвращает профиль пользователя"""
    async with ClientSession() as session:
        photo = await s3_client.get_object(bucket_name=user.username,
                                           object_name=f'ava_{user.username}.png',
                                           session=session)

    return GetMeUser(id=user.id, username=user.username, phone=user.phone,
                     url=str(photo.url).replace('minio', 'localhost'),  # пока оставлю костыль
                     register_data=user.register_data, is_active=user.is_active, is_superuser=user.is_superuser,
                     is_verified=user.is_verified)


@router.put("/update/avatar/", status_code=status.HTTP_201_CREATED)
async def update_avatar(photo: UploadFile,
                        user: Users = Depends(get_current_user)):
    """Добавляет аватарку пользователю"""
    await s3_client.add_avatar(photo=photo, username=user.username)
    return {"success": "Добавлено фото профиля"}


@router.patch('/update/me/profile/')
async def update_auth_user(component: Dict = Depends(get_auth_user_and_session)):
    """Функция не работает"""
    return "Функция заглушка"


@router.delete('/delete/me/profile/')
async def delete_auth_user(component: Dict = Depends(get_auth_user_and_session)):
    """Удаление авторизованного пользователя"""
    await delete_user_db(username=component['user'].username, session=component['session'])
    await s3_client.remove_bucket(component['user'].username)
    return {"success": "Пользователь успешно удален"}


@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(user: RegisterUser,
                        session: AsyncSession = Depends(get_async_session)):
    """Регистрация пользователя на сайте"""
    await exists_user_by_phone(user.phone, session)  # проверяем наличие юзера с таким номером телефона
    hashed_password = Hasher.get_password_hash(user.password_1)  # получаем hash нового пароля
    await add_user_in_database(user.username, user.phone, hashed_password, session)  # добавляем пользователя
    await s3_client.make_bucket(user.username)  # создает bucket по username
    await s3_client.add_default_avatar(username=user.username, filename=make_default_png(username=user.username))
    return {"success": "Пользователь успешно зарегистрирован!"}


@router.post("/change-password/")
async def change_password(password: ChangePassword,
                          user: Users = Depends(basic_auth_validate),  # текущий пользователь
                          session: AsyncSession = Depends(get_async_session)):
    """Функция смены пароля"""
    # Проверка паролей
    if not Hasher.verify_password(
            plain_password=password.old_password,
            hashed_password=user.hashed_password):  # сравниваем полученный пароль со старым
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Неверный старый пароль")
    # Обновление пароля
    new_hashed_password = Hasher.get_password_hash(password.password_1)  # получаем hash нового пароля
    await change_password_db(username=user.username,
                             new_hash_password=new_hashed_password,
                             session=session)
    return {"success": "Пароль успешно изменен!"}

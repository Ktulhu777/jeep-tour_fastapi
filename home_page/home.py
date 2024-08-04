from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database_engine import get_async_session
from .database_service import get_attractions, add_attraction_in_db
from .schema import GetAttractionsSchema, PostAttractionsSchema

router = APIRouter()


@router.get('/')
async def get_home_page(session: AsyncSession = Depends(get_async_session)):
    all_attractions = await get_attractions(session)
    if all_attractions:
        return [GetAttractionsSchema(id=i.id, title=i.title) for i in all_attractions]
    return "Empty"


@router.post('/add-attraction/', status_code=status.HTTP_201_CREATED)
async def add_attraction(attraction: PostAttractionsSchema,
                         session: AsyncSession = Depends(get_async_session)):
    await add_attraction_in_db(attraction.title, attraction.description, session)
    return 'ok'

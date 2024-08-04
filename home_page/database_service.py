from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.models import Attractions


async def get_attractions(session: AsyncSession):
    all_attractions = await session.execute(select(Attractions))
    return all_attractions.scalars().all()


async def add_attraction_in_db(title: str, description: str, session: AsyncSession):
    one_attraction = Attractions(title=title, description=description)
    session.add(one_attraction)
    await session.commit()
    await session.refresh(one_attraction)

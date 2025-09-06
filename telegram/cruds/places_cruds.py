from db import AsyncSessionLocal, PlaceModel
from sqlalchemy import select, and_

async def get_places(place_type: str, city: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(PlaceModel)
            .where(
                and_(
                PlaceModel.name == place_type,
                PlaceModel.address == city,
            )))
    return result.scalars().all()
from db import AsyncSessionLocal, PlaceModel
from sqlalchemy import select, and_, distinct

async def get_places(place_type: str, city: str) -> list[PlaceModel]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(PlaceModel)
            .where(
                and_(
                PlaceModel.name == place_type,
                PlaceModel.address == city,
            )))
    return result.scalars().all()

async def get_unique_places(city: str) -> list[str]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(distinct(
                PlaceModel.name
            ).where(PlaceModel.city == city)
        ))

    return [row[0] for row in result.all()]

async def get_unique_cities() -> list[str]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(distinct(PlaceModel.city))
        )
    return [row[0] for row in result.all()]

from sqlalchemy import select, func, desc
from db import AsyncSessionLocal, CodeModel, PlaceModel

async def get_code_by_place_addr(address: str) -> CodeModel | None:
    subq = (
        select(CodeModel.id)
        .join(PlaceModel, CodeModel.place_id == PlaceModel.id)
        .where(PlaceModel.address == address)
        .order_by(desc(CodeModel.created_at))
        .limit(1)
    )

    stmt = (
        select(CodeModel)
        .where(CodeModel.id.in_(subq))
    )
    async with AsyncSessionLocal() as session:
        return await session.execute(stmt).scalar_one_or_none()
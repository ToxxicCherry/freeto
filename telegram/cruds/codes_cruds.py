from sqlalchemy import select, func, desc
from db import AsyncSessionLocal, CodeModel, PlaceModel, UserModel

async def get_code_by_place_addr(address: str) -> CodeModel | None:
    subq = (
        select(CodeModel.id)
        .join(PlaceModel, CodeModel.place_id == PlaceModel.id)
        .where(PlaceModel.address == address)
        .order_by(desc(CodeModel.created_at))
        .limit(1)
        .scalar_subquery()
    )

    stmt = (
        select(CodeModel)
        .where(CodeModel.id.in_(subq))
    )
    async with AsyncSessionLocal() as session:
        result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def add_code_to_place(address: str, user_tg_id: str, code: int):
    subq_place = select(PlaceModel.id).where(PlaceModel.address == address).scalar_subquery()
    subq_user = select(UserModel.id).where(UserModel.tg_id == user_tg_id).scalar_subquery()

    new_code = CodeModel(
        place_id=subq_place,
        user_id=subq_user,
        code=code
    )

    async with AsyncSessionLocal() as session:
        session.add(new_code)
        await session.commit()
from sqlalchemy.exc import IntegrityError
from db import UserModel, AsyncSessionLocal

async def create_user(tg_id: str, username: str = None):
    user = UserModel(tg_id=tg_id, username=username)
    async with AsyncSessionLocal() as session:
        session.add(user)
        try:
            await session.commit()
            return True
        except IntegrityError:
            await session.rollback()
            return False
        except Exception as e:
            print('Ошибка при добавлении записи в БД', e, sep='\n')
            return False


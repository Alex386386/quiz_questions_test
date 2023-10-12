import random
from typing import List

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Question


class CRUDQuestion(CRUDBase):

    async def create_with_id(self, obj_in: dict, session: AsyncSession):
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def bulk_create(self, objs_in: List[dict], session: AsyncSession):
        db_objs = [self.model(**obj) for obj in objs_in]
        session.add_all(db_objs)
        await session.commit()

    async def get_by_id(self, question_id: int, session: AsyncSession):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == question_id)
        )
        return db_obj.scalars().first()

    async def get_all_ids(self, session: AsyncSession):
        result = await session.execute(select(self.model.id))
        return result.scalars().all()

    async def delete_all(self, session: AsyncSession):
        await session.execute(delete(self.model))
        await session.commit()

    async def get_last_downloaded_question(self, session: AsyncSession):
        last_question = await session.execute(
            select(self.model).order_by(self.model.downloaded_at.desc()).limit(1)
        )
        return last_question.scalars().first()

    async def get_random_question(self, session: AsyncSession):
        all_ids = await self.get_all_ids(session)

        if not all_ids:
            return None

        random_id = random.choice(all_ids)

        return await self.get_by_id(random_id, session)


question_crud = CRUDQuestion(Question)

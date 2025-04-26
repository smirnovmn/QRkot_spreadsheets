from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, User
from app.models.charity_project import CharityProject

from .base import CRUDBase


class CRUDProject(CRUDBase):

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        if 'full_amount' in update_data:
            new_amount = update_data['full_amount']
            if new_amount < db_obj.invested_amount:
                raise HTTPException(
                    status_code=422,
                    detail=(
                        'Нельзя установить требуемую'
                        'сумму меньше уже вложенной'
                    )
                )
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if (
            not db_obj.fully_invested and
            db_obj.invested_amount >= db_obj.full_amount
        ):
            db_obj.fully_invested = True
            db_obj.close_date = datetime.utcnow()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, int]]:
        duration = (
            func.julianday(CharityProject.close_date) -
            func.julianday(CharityProject.create_date)
        )
        result = await session.execute(
            select(
                CharityProject,
                duration.label("duration_days")
            ).where(
                CharityProject.fully_invested.is_(True)
            ).order_by(duration)
        )
        result = result.all()
        res = [
            {
                "project_id": project.id,
                "name": project.name,
                "descr": project.description,
                "duration_days": round(duration_days, 2)
            }
            for project, duration_days in result
        ]
        return res


project_crud = CRUDProject(CharityProject)

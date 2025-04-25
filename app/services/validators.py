from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constans import MINIMAL_INV_AMOUNT
from app.models import CharityProject
from app.models.charity_project import CharityProject


async def check_is_full_amount_project(
    project: CharityProject,
    session: AsyncSession,
):
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Редактировать проинвестированный проект нельзя!'
        )
    return project


async def check_name_dublicate(
    name: str,
    session: AsyncSession,
):
    result = await session.execute(
        select(CharityProject).where(CharityProject.name == name)
    )
    existing_project = result.scalars().first()
    if existing_project:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует.'
        )


async def check_project_is_invested(
    charity_project: CharityProject,
):
    if charity_project.invested_amount != MINIMAL_INV_AMOUNT:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def check_is_name_exist(
        obj_name: str,
        session: AsyncSession,
):
    result = await session.execute(
        select(CharityProject).where(CharityProject.name == obj_name)
    )
    result = result.scalars().first()
    if result is not None:
        raise HTTPException(
            status_code=400,
            detail='Это имя уже используется!',
        )
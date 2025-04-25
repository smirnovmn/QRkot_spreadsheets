from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud


async def get_obj_or_404(
    project_id: int,
    session: AsyncSession
):
    project = await project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект с данным id не найден'
        )
    return project

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import get_obj_or_404
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.models import User
from app.schemas.charity_project import (CharityProjectBase, CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.management_service import (create_new_project,
                                             project_delete, project_update)

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_project(
        session: AsyncSession = Depends(get_async_session),
):
    projects = await project_crud.get_multi(session)
    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_projects(
        project: CharityProjectBase,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_superuser),
):
    new_project = await create_new_project(project, user, session)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_superuser),
):
    project = await get_obj_or_404(project_id, session)
    project = await project_delete(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await get_obj_or_404(project_id, session)
    project = await project_update(project, obj_in, session)
    return project

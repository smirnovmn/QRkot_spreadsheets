from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.user import User
from app.schemas.charity_project import CharityProjectUpdate
from app.services.distribution_service import distribution_method
from app.services.validators import (check_is_full_amount_project,
                                     check_is_name_exist, check_name_dublicate,
                                     check_project_is_invested)


async def create_new_project(
    project: CharityProject,
    user: User,
    session: AsyncSession,
):
    await check_name_dublicate(project.name, session)
    new_project = await project_crud.create(project, session, user=user)
    await distribution_method(new_project, Donation, session)
    return new_project


async def create_new_donation(
    donation: Donation,
    user: User,
    session: AsyncSession,
):
    new_donation = await donation_crud.create(donation, session, user=user)
    await distribution_method(new_donation, CharityProject, session)
    return new_donation


async def project_update(
    project: CharityProject,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
):
    project = await check_is_full_amount_project(project, session)
    if obj_in.name and obj_in.name != project.name:
        await check_is_name_exist(obj_in.name, session)
    project = await project_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session,
    )
    return project


async def project_delete(
    project: CharityProject,
    session: AsyncSession,
):
    await check_project_is_invested(project)
    project = await project_crud.remove(
        project, session
    )
    return project

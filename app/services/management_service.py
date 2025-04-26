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


class Management:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_new_project(
        self,
        project: CharityProject,
        user: User
    ):
        await check_name_dublicate(project.name, self.session)
        new_project = await project_crud.create(
            project, self.session, user=user
        )
        await distribution_method(new_project, Donation, self.session)
        return new_project

    async def create_new_donation(
        self,
        donation: Donation,
        user: User,
    ):
        new_donation = await donation_crud.create(
            donation, self.session, user=user
        )
        await distribution_method(new_donation, CharityProject, self.session)
        return new_donation

    async def project_update(
        self,
        project: CharityProject,
        obj_in: CharityProjectUpdate,
    ):
        project = await check_is_full_amount_project(project, self.session)
        if obj_in.name and obj_in.name != project.name:
            await check_is_name_exist(obj_in.name, self.session)
        project = await project_crud.update(
            db_obj=project,
            obj_in=obj_in,
            session=self.session,
        )
        return project

    async def project_delete(
        self,
        project: CharityProject,
    ):
        await check_project_is_invested(project)
        project = await project_crud.remove(
            project, self.session
        )
        return project

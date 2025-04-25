from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, User
from app.models.donation import Donation

from .base import CRUDBase


class CRUDDonation(CRUDBase):

    def __init__(self, model):
        self.model = model

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        if 'create_date' not in obj_in_data:
            obj_in_data['create_date'] = datetime.now()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_all_my_donations(
            self,
            session: AsyncSession,
            user: User,
    ):
        db_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return db_donations.scalars().all()


donation_crud = CRUDDonation(Donation)

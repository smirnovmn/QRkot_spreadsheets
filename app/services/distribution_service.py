from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.constans import MINIMAL_INV_AMOUNT


async def distribution_method(obj_in, db_obj, session: AsyncSession):
    result = await session.execute(
        select(db_obj).filter(
            db_obj.fully_invested.is_(False)
        ).order_by(db_obj.create_date)
    )
    all_result = result.scalars().all()
    if not all_result:
        return
    amount = obj_in.full_amount
    obj_in.invested_amount = MINIMAL_INV_AMOUNT
    for target_obj in all_result:
        free_for_target = target_obj.full_amount - target_obj.invested_amount
        if amount >= free_for_target:
            target_obj.invested_amount = target_obj.full_amount
            target_obj.fully_invested = True
            target_obj.close_date = datetime.now()
            obj_in.invested_amount += free_for_target
            amount -= free_for_target
        else:
            target_obj.invested_amount += amount
            obj_in.invested_amount += amount
            amount = MINIMAL_INV_AMOUNT
            break
    if amount == MINIMAL_INV_AMOUNT:
        obj_in.fully_invested = True
        obj_in.close_date = datetime.now()
    await session.commit()
    await session.refresh(obj_in)
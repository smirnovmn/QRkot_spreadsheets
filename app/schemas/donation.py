from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    comment: Optional[str] = None
    full_amount: PositiveInt


class DonationCreate(DonationBase):
    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    user_id: int
    invested_amount: int
    fully_invested: bool
    id: int
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class DonationDB2(DonationBase):
    """ Альтернативная схема ответа. """
    id: int
    create_date: datetime

    class Config:
        orm_mode = True

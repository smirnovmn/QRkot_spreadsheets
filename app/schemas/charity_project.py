from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.constans import (DESCRIPTION_MAX_LEN, DESCRIPTION_MIN_LEN,
                          NAME_MAX_LEN, NAME_MIN_LEN)

CURRENT_DATE = datetime.now()


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=NAME_MIN_LEN, max_length=NAME_MAX_LEN)
    description: str = Field(
        ..., min_length=DESCRIPTION_MIN_LEN, max_length=DESCRIPTION_MAX_LEN
    )
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=NAME_MIN_LEN, max_length=NAME_MAX_LEN
    )
    description: Optional[str] = Field(
        None, min_length=DESCRIPTION_MIN_LEN, max_length=DESCRIPTION_MAX_LEN
    )
    full_amount: Optional[PositiveInt]

    class Config:
        orm_mode = True
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.constans import DEFAULT_INV_AMOUNT, NAME_MAX_LEN
from app.core.db import Base


class CharityProject(Base):
    name = Column(String(NAME_MAX_LEN), unique=True)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=DEFAULT_INV_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

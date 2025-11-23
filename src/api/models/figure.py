from sqlmodel import SQLModel, Field
from typing import Optional


class Figure(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    description: Optional[str] = None

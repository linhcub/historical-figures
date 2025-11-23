from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import Column, Text, String


class Figure(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    title: Optional[str] = Field(default=None, max_length=256, sa_column=Column(String(256)))
    era: Optional[str] = Field(default=None, max_length=128, sa_column=Column(String(128)))
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    introduction: Optional[str] = Field(default=None, sa_column=Column(Text))
    biography: Optional[str] = Field(default=None, sa_column=Column(Text))
    contributions: Optional[str] = Field(default=None, sa_column=Column(Text))
    image_intro: Optional[str] = Field(default=None, max_length=256, sa_column=Column(String(256)))
    image_activity: Optional[str] = Field(default=None, max_length=256, sa_column=Column(String(256)))
    image_ext_1: Optional[str] = Field(default=None, max_length=256, sa_column=Column(String(256)))
    image_ext_2: Optional[str] = Field(default=None, max_length=256, sa_column=Column(String(256)))
    video_1: Optional[str] = Field(default=None, max_length=256, sa_column=Column(String(256)))
    video_2: Optional[str] = Field(default=None, max_length=256, sa_column=Column(String(256)))

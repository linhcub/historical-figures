from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from api.config.db_async import get_async_session
from api.models.figure import Figure

router = APIRouter()

@router.get("/figures", response_model=List[Figure])
async def get_figures(session: AsyncSession = Depends(get_async_session)):
    try:
        statement = select(Figure).limit(10)
        result = await session.execute(statement)
        figures = result.scalars().all()
        return figures
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

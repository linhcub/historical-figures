from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, SQLModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from api.config.db_async import get_async_session
from api.models.figure import Figure

router = APIRouter()

# Lightweight response model for list endpoint — expose introduction instead of short_summary
class FigureSummary(SQLModel):
    id: int
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    introduction: Optional[str] = None
    image_intro: Optional[str] = None

@router.get("/figures", response_model=List[FigureSummary])
async def get_figures(session: AsyncSession = Depends(get_async_session)):
    try:
        # select only the fields we want to expose in the list view
        statement = select(
            Figure.id,
            Figure.name,
            Figure.birth_year,
            Figure.death_year,
            Figure.introduction,
            Figure.image_intro,
        ).limit(10)
        result = await session.execute(statement)
        rows = result.all()
        # rows are tuples in the same order as selected columns
        summaries = [
            FigureSummary(
                id=r[0],
                name=r[1],
                birth_year=r[2],
                death_year=r[3],
                introduction=r[4],
                image_intro=r[5],
            )
            for r in rows
        ]
        return summaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/figures/{figure_id}", response_model=Figure)
async def get_figure(figure_id: int, session: AsyncSession = Depends(get_async_session)):
    """Return details for a single Figure by id."""
    try:
        statement = select(Figure).where(Figure.id == figure_id)
        result = await session.execute(statement)
        figure = result.scalars().one_or_none()
        if figure is None:
            raise HTTPException(status_code=404, detail="Figure not found")
        return figure
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

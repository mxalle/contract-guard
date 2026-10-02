from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

router = APIRouter()

@router.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness_check(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict:
    try:
        await session.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="database unavailable")
    return {"status": "ready"}
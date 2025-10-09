from fastapi import APIRouter

from app.api import cursos
from app.api import professores

api_router = APIRouter()

api_router.include_router(cursos.router, prefix="/cursos", tags=["cursos"])
api_router.include_router(
    professores.router, 'prefix/professores', tags=["professores"]
)

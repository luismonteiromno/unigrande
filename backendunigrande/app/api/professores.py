from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, Response, status
from tortoise.exceptions import (DoesNotExist, IntegrityError,
                                 MultipleObjectsReturned)
from tortoise.transactions import in_transaction

from app.auth.utils import setup_logger
from app.schemas.unigrande import ProfessorCreate, ProfessorResponse, ProfessorUpdate
from app.services.unigrande import ProfessorService

# Configurar o logger
logger = setup_logger()

router = APIRouter()


# =============== util de erro ===============
async def error_500(e: Exception):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Ocorreu um erro inesperado: {str(e)}",
    )


# ----------------------------------------------------------------------
# Professor
# ----------------------------------------------------------------------
@router.post("/create-professor", response_model=ProfessorResponse, status_code=201)
async def create_professor(payload: ProfessorCreate):
    async with in_transaction():
        try:
            obj = await ProfessorService.create(payload)
            return await ProfessorService.response(obj)
        except IntegrityError as e:
            raise HTTPException(409, f"Restrição de integridade: {e}")
        except Exception as e:
            await error_500(e)


@router.get("/buscar-professores/{id}", response_model=ProfessorResponse)
async def get_professores(id: int):
    try:
        obj = await ProfessorService.get(id)
        return await ProfessorService.response(obj)
    except (DoesNotExist, MultipleObjectsReturned):
        raise HTTPException(404, "Professor não encontrado")
    except Exception as e:
        await error_500(e)


@router.get("/listar-professores", response_model=List[ProfessorResponse])
async def list_professores():
    try:
        rows = await ProfessorService.list_all()
        return [await ProfessorService.response(x) for x in rows]
    except Exception as e:
        await error_500(e)


@router.put("/atualizar-professor/{id}", response_model=ProfessorResponse)
async def update_professor(id: int, payload: ProfessorUpdate):
    async with in_transaction():
        try:
            obj = await ProfessorService.update(id, payload)
            return await ProfessorService.response(obj)
        except HTTPException as e:
            raise e
        except Exception as e:
            await error_500(e)


@router.delete("/delete-professor/{id}", status_code=204)
async def delete_professor(id: int):
    async with in_transaction():
        try:
            await ProfessorService.delete(id)
            return Response(status_code=204)
        except HTTPException as e:
            raise e
        except Exception as e:
            await error_500(e)

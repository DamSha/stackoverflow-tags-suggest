from fastapi import (  # Depends,; FastAPI,; HTTPException,; Response,; status,
    APIRouter,
)

from app.api import schemas

# from starlette.requests import Request


router = APIRouter(
    prefix="",
    tags=['Root']
)


@router.get("/", response_model=schemas.SimpleResponse)
def root():
    response = schemas.SimpleResponse(
        status="OK",
        message="Bienvenue sur l'API de suggestion de Tags pour Stackoverflow")
    return response


@router.get('/health-check', response_model=schemas.SimpleResponse)
async def health_check():
    response = schemas.SimpleResponse(
        status="OK",
        message="Health-Check OK.")
    return response

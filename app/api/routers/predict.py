from fastapi import (  # Depends,; FastAPI,; HTTPException,; Response,; status,
    APIRouter,
)
from starlette.requests import Request

from app.api import schemas

router = APIRouter(
    prefix="/predict",
    tags=['Predict']
)


@router.post('/', response_model=schemas.PredictOutput)
async def predict(request: Request, question: schemas.QuestionInput):
    raise NotImplementedError("Développement en cours.")


@router.post('/test', response_model=schemas.PredictOutput)
async def predict_test(request: Request, question: schemas.QuestionInput):
    prediction = schemas.PredictOutput()
    prediction.tags = ["Python", "FastAPI"]
    return prediction

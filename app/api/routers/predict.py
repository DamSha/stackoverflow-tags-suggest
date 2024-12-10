from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.api import schemas
from app.suggestor.suggestor import Suggestor

router = APIRouter(
    prefix="/predict",
    tags=['Predict']
)


@router.post('/', response_model=schemas.PredictOutput)
async def predict_supervised(question: schemas.QuestionInput):
    try:
        results_s = Suggestor().predict(question.title, question.body, .1)
    except Exception:  # pragma: no cover
        # Retourne [[]]
        return JSONResponse(content=[[]])  # pragma: no cover
    if results_s is None:
        # Retourne [[]]
        return JSONResponse(content=[[]])
    # Prédictions
    predictions_s = [[f"{p["tag"]}", round(p["proba"], 3)]
                     for p in results_s.to_dict(orient="records")]
    # Retourne les prédictions
    return JSONResponse(content=jsonable_encoder(predictions_s))


@router.post('/test', response_model=schemas.PredictOutput)
async def predict_test(question: schemas.QuestionInput):
    # print(question)
    prediction = schemas.PredictOutput()
    prediction.tags = [["Python", 0.754], ["FastAPI", 0.456]]
    return JSONResponse(content=jsonable_encoder(prediction.tags))

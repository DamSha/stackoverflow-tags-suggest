from pydantic import BaseModel


class QuestionInput(BaseModel):
    title: str
    body: str


class PredictOutput(BaseModel):
    tags: list = [[str, float]]


class SimpleResponse(BaseModel):
    status: str
    message: str

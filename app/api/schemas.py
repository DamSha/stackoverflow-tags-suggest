from pydantic import BaseModel


class QuestionInput(BaseModel):
    title: str
    content: str

class PredictOutput(BaseModel):
    tags: list
    timing: str


class SimpleResponse(BaseModel):
    status: str
    message: str
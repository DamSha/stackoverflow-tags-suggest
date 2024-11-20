from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.api import schemas
from app.api.facade import app


# Utilisation de TestClient pour tester l'application FastAPI
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_post_predict_test(client):
    """ Test predict """
    question = schemas.QuestionInput(title="Titre Question 1", body="Texte question 1")
    response = client.post("/predict/test", content=question.model_dump_json())
    assert response.status_code == 200


def test_get_predict(client):
    """ Test GET /predict """
    response = client.get("/predict")
    assert response.status_code == 405

def test_post_predict_empty(client):
    """ Test POST /predict empty """
    response = client.post("/predict")
    assert response.status_code == 422

def test_post_predict_notimplemented(client):
    """ Test POST /predict NotImplementedError
    TODO : supprimer quand implémenté """
    question = schemas.QuestionInput(title="Titre Question 1", body="Texte question 1")
    with pytest.raises(NotImplementedError):
        client.post("/predict", content=question.model_dump_json())

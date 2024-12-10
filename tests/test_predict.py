import pandas as pd
import pytest

# from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import schemas
from app.api.facade import app
from app.suggestor.suggestor import Suggestor


# Utilisation de TestClient pour tester l'application FastAPI
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_post_predict_test(client):
    """ Test predict """
    question = schemas.QuestionInput(title="Titre Question 1",
                                     body="Texte question 1")
    response = client.post("/predict/test",
                           content=question.model_dump_json())
    assert response.status_code == 200


def test_get_predict(client):
    """ Test GET /predict """
    response = client.get("/predict")
    assert response.status_code == 405


def test_post_predict_empty(client):
    """ Test POST /predict empty """
    response = client.post("/predict")
    assert response.status_code == 422


def test_post_predict_ok(client):
    """ Test POST /predict
    TODO : supprimer quand implémenté """
    question = schemas.QuestionInput(title="Titre Question 1",
                                     body="Texte question 1")
    response = client.post("/predict",
                           content=question.model_dump_json())
    assert response.status_code == 200


@pytest.fixture
def suggestor():
    return Suggestor()


def test_predict_basic():
    suggestor = Suggestor()
    title = "How to parse JSON in Python?"
    body = ("I'm trying to parse JSON data in Python "
            "but getting errors. Here's my code...")
    threshold = 0.1

    results = suggestor.predict(title, body, threshold)

    assert isinstance(results, pd.DataFrame)
    assert 'tag' in results.columns
    assert 'proba' in results.columns
    assert all(results['proba'] >= threshold)


def test_predict_empty_input():
    suggestor = Suggestor()
    title = ""
    body = ""
    threshold = 0.1

    results = suggestor.predict(title, body, threshold)

    assert results is None

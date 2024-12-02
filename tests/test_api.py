import time

import pytest

# from fastapi import FastAPI
from fastapi.testclient import TestClient

# from app.api import schemas
from app.api.facade import app


# Utilisation de TestClient pour tester l'application FastAPI
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.mark.api
def test_root(client):
    """ Test de la route ROOT """
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.api
def test_health_check(client):
    """ Test de la route /health-check """
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "message": "Health-Check OK."}


@pytest.mark.api
def test_rate_api(client):
    """ Test du Rate Limiter de l'API """
    # lancement de 2 appels API simultannées
    t1 = time.perf_counter()
    for n in range(3):
        response = client.get("/health-check")
        # assert response.status_code == 200
    # le 3e test doit être limité
    response = client.get("/health-check")
    t2 = time.perf_counter()
    assert t2 - t1 < 1
    assert response.status_code == 429

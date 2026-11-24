"""CI 에서 이미지를 만들기 전에 도는 시험. 모델을 임시 폴더에 직접 학습해서 쓰니 파일이 없어도 돼요."""
import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from train import train


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    out = tmp_path_factory.mktemp("model")
    train(out)
    with TestClient(create_app(str(out / "model.joblib"))) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "model_loaded": True}


def test_predict_setosa(client):
    r = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert r.status_code == 200
    assert r.json()["label"] == "setosa"


def test_predict_virginica(client):
    r = client.post("/predict", json={"features": [6.7, 3.0, 5.2, 2.3]})
    assert r.json()["label"] == "virginica"


def test_wrong_length_is_422(client):
    r = client.post("/predict", json={"features": [1.0, 2.0]})
    assert r.status_code == 422


def test_health_503_without_model(tmp_path):
    with TestClient(create_app(str(tmp_path / "none.joblib"))) as c:
        assert c.get("/health").status_code == 503

"""붓꽃 품종 추론 API (FastAPI).

- GET  /health   살아 있는지, 모델을 불러왔는지
- POST /predict  {"features": [꽃받침 길이, 꽃받침 너비, 꽃잎 길이, 꽃잎 너비]} -> 품종
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    features: list[float] = Field(min_length=4, max_length=4, examples=[[5.1, 3.5, 1.4, 0.2]])


def create_app(model_path: str | None = None) -> FastAPI:
    path = Path(model_path or os.environ.get("MODEL_PATH", "model/model.joblib"))
    state: dict = {}

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        if path.exists():
            state["bundle"] = joblib.load(path)
        yield
        state.clear()

    app = FastAPI(title="iris-service", lifespan=lifespan)

    @app.get("/health")
    def health():
        loaded = "bundle" in state
        if not loaded:
            raise HTTPException(status_code=503, detail="model not loaded")
        return {"status": "ok", "model_loaded": True}

    @app.post("/predict")
    def predict(req: PredictRequest):
        bundle = state.get("bundle")
        if bundle is None:
            raise HTTPException(status_code=503, detail="model not loaded")
        model = bundle["model"]
        proba = model.predict_proba([req.features])[0]
        idx = int(proba.argmax())
        return {
            "label": bundle["target_names"][idx],
            "probability": round(float(proba[idx]), 4),
        }

    return app


app = create_app()

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, field_validator
import joblib

def _load_model():
    base_dir = Path(__file__).resolve().parent.parent
    model_path = base_dir / "model_pipeline.pkl"
    print("LOADING MODEL FROM:", model_path)
    return joblib.load(model_path)

_MODEL = _load_model()

lab_app = FastAPI(title="Housing Prediction Sub-App")


class HousingFeatures(BaseModel):
    model_config = ConfigDict(extra="forbid")

    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

    @field_validator("Latitude")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        if not (-90.0 <= v <= 90.0):
            raise ValueError("Invalid value for Latitude")
        return v

    @field_validator("Longitude")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        if not (-180.0 <= v <= 180.0):
            raise ValueError("Invalid value for Longitude")
        return v


class PredictionResponse(BaseModel):
    prediction: float






@lab_app.get("/health")
def health() -> dict[str, str]:
    now = datetime.now(timezone.utc).isoformat()
    return {"time": now}


@lab_app.get("/hello")
def hello(name: str) -> dict[str, str]:
    return {"message": f"Hello {name}"}


@lab_app.post("/predict", response_model=PredictionResponse)
def predict(features: HousingFeatures) -> PredictionResponse:
    x = np.array(
        [[
            features.MedInc,
            features.HouseAge,
            features.AveRooms,
            features.AveBedrms,
            features.Population,
            features.AveOccup,
            features.Latitude,
            features.Longitude,
        ]],
        dtype=float,
    )

    y_pred = _MODEL.predict(x)
    pred_value = float(y_pred[0])
    return PredictionResponse(prediction=pred_value)

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
from datetime import date
import joblib
import pandas as pd


saved = joblib.load('models/random_forest.joblib')
rf_model = saved['model']
feature_columns = saved['feature_columns']

app = FastAPI(title="Nexora Appointment Forecasting API")

class ForecastRequest(BaseModel):
    clinic: Literal["Lakeside", "Riverside", "Downtown Express", "Hillcrest"] = Field(example="Lakeside")
    forecast_date: date = Field(example="2026-11-24")
    is_holiday: bool = Field(example=False)
    season_flag: Literal["Flu Season", "Allergy Season", "Standard"] = Field(example="Flu Season")

@app.post("/predict") 
def predict_volume(request: ForecastRequest) -> dict:
    data = pd.DataFrame([{
        "Clinic": request.clinic,
        "IsHoliday": int(request.is_holiday),
        "SeasonFlag": request.season_flag,
        "dow": pd.Timestamp(request.forecast_date).dayofweek,
    }])

    data = pd.get_dummies(data, columns=["Clinic", "SeasonFlag", "dow"], dtype=float)

    data = data.reindex(columns=feature_columns, fill_value=0)

    pred = max(0.0, float(rf_model.predict(data)[0]))

    return {
        "clinic": request.clinic,
        "date": str(request.forecast_date),
        "predicted_appointments": round(pred),
    }

from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "attrition_pipeline.joblib"

THRESHOLD = 0.446
MODEL_VERSION = "1.0.0"


pipeline = joblib.load(MODEL_PATH)


def predict_attrition(employee_data: dict):
    df = pd.DataFrame([employee_data])

    probability = float(
        pipeline.predict_proba(df)[0, 1]
    )

    prediction = probability >= THRESHOLD

    return {
        "probability": probability,
        "prediction": prediction,
        "threshold": THRESHOLD,
        "model_version": MODEL_VERSION,
    }
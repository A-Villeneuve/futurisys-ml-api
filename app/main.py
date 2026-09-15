from fastapi import FastAPI

from app.schemas import EmployeeInput, PredictionResponse


app = FastAPI(
    title="Futurisys ML API",
    description="API de prédiction du risque d'attrition des employés",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")

def predict(employee: EmployeeInput):

    return employee
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.db_models import (
    Employee,
    Model,
    PredictionRequest,
    PredictionResult,
    User,
    UserAction,
)
from app.ml.predictor import predict_attrition
from app.schemas import EmployeeCreate, EmployeeInput, PredictionResponse


app = FastAPI(
    title="Futurisys ML API",
    description="API de prédiction du risque d'attrition des employés",
    version="0.1.0",
)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "model": "loaded",
        }

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
            },
        ) from exc



@app.post("/employees", status_code=201)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        # Vérifie que l'identifiant n'existe pas déjà
        existing_employee = db.get(Employee, employee.id_employee)

        if existing_employee is not None:
            raise HTTPException(
                status_code=409,
                detail="Un employé avec cet identifiant existe déjà.",
            )

        # Création de l'employé
        new_employee = Employee(
            **employee.model_dump()
        )

        db.add(new_employee)
        db.flush()

        # Traçabilité de l'action
        action = UserAction(
            user_id=current_user.id,
            action="CREATE",
            resource_type="employee",
            resource_id=str(new_employee.id_employee),
        )

        db.add(action)

        # Employé + audit validés dans la même transaction
        db.commit()

        return {
            "id_employee": new_employee.id_employee,
            "message": "Employé créé avec succès.",
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la création de l'employé.",
        ) from exc


@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        # Recherche de l'employé
        employee = db.get(Employee, employee_id)

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employé introuvable.",
            )

        # Suppression de l'employé
        db.delete(employee)

        # Conservation de la trace de la suppression
        action = UserAction(
            user_id=current_user.id,
            action="DELETE",
            resource_type="employee",
            resource_id=str(employee_id),
        )

        db.add(action)

        # Suppression + audit validés ensemble
        db.commit()

        return {
            "id_employee": employee_id,
            "message": "Employé supprimé avec succès.",
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la suppression de l'employé.",
        ) from exc


@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(
    employee: EmployeeInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        employee_data = employee.model_dump()

        # 1. Récupération du modèle utilisé
        model = db.scalar(
            select(Model).where(Model.version == "1.0.0")
        )

        if model is None:
            raise HTTPException(
                status_code=500,
                detail="Modèle non enregistré en base de données.",
            )

        # 2. Enregistrement de l'entrée de prédiction
        request = PredictionRequest(
            **employee_data
        )

        db.add(request)
        db.flush()

        # 3. Appel du modèle ML
        model_output = predict_attrition(
            employee_data
        )

        # 4. Enregistrement du résultat
        result = PredictionResult(
            request_id=request.id,
            model_id=model.id,
            probability=model_output["probability"],
            prediction=model_output["prediction"],
            threshold=model_output["threshold"],
        )

        db.add(result)
        db.flush()

        # 5. Enregistrement de l'action utilisateur
        action = UserAction(
            user_id=current_user.id,
            action="PREDICT",
            resource_type="prediction",
            resource_id=str(result.id),
        )

        db.add(action)

        # 6. Validation de toute la transaction
        db.commit()

        return PredictionResponse(
            prediction_id=result.id,
            probability=result.probability,
            prediction=result.prediction,
            threshold=result.threshold,
        )

    except HTTPException:
        db.rollback()
        raise

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la prédiction.",
        ) from exc
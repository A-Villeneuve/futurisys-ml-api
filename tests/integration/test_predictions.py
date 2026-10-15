from sqlalchemy import select

from app.db_models import (
    PredictionRequest,
    PredictionResult,
    UserAction,
)
from tests.conftest import TestSessionLocal


def valid_prediction_data():
    return {
        "age": 30,
        "genre": "M",
        "statut_marital": "Célibataire",
        "distance_domicile_travail": 10,
        "departement": "Consulting",
        "poste": "Consultant",
        "niveau_hierarchique_poste": 2,
        "revenu_mensuel": 3500,
        "augementation_salaire_precedente": 10,
        "nombre_participation_pee": 1,
        "nombre_experiences_precedentes": 2,
        "annee_experience_totale": 6,
        "annees_dans_l_entreprise": 3,
        "annees_dans_le_poste_actuel": 2,
        "annees_depuis_la_derniere_promotion": 1,
        "annes_sous_responsable_actuel": 2,
        "satisfaction_employee_environnement": 3,
        "satisfaction_employee_nature_travail": 3,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "note_evaluation_precedente": 3,
        "note_evaluation_actuelle": 4,
        "heure_supplementaires": "Non",
        "frequence_deplacement": "Occasionnel",
        "niveau_education": 3,
        "domaine_etude": "Transformation Digitale",
        "nb_formations_suivies": 2,
    }


def test_predict_requires_api_key(client):
    response = client.post(
        "/predict",
        json=valid_prediction_data(),
    )

    assert response.status_code == 401


def test_predict_rejects_invalid_data(client, auth_headers):
    data = valid_prediction_data()
    data["age"] = 12

    response = client.post(
        "/predict",
        json=data,
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_predict_returns_prediction(client, auth_headers):
    response = client.post(
        "/predict",
        json=valid_prediction_data(),
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["prediction_id"] > 0
    assert 0 <= body["probability"] <= 1
    assert isinstance(body["prediction"], bool)
    assert body["threshold"] == 0.446


def test_prediction_is_stored_and_audited():
    with TestSessionLocal() as db:
        request = db.scalar(
            select(PredictionRequest)
            .order_by(PredictionRequest.id.desc())
        )

        result = db.scalar(
            select(PredictionResult)
            .order_by(PredictionResult.id.desc())
        )

        action = db.scalar(
            select(UserAction)
            .where(UserAction.action == "PREDICT")
            .order_by(UserAction.id.desc())
        )

        assert request is not None
        assert result is not None
        assert action is not None

        assert result.request_id == request.id
        assert result.model_id == 1
        assert 0 <= result.probability <= 1
        assert result.threshold == 0.446

        assert action.resource_type == "prediction"
        assert action.resource_id == str(result.id)


def test_predict_rejects_invalid_api_key(client):
    response = client.post(
        "/predict",
        json=valid_prediction_data(),
        headers={
            "X-API-Key": "invalid-api-key",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Clé API invalide.",
    }
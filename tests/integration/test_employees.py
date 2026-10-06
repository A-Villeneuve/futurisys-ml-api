from sqlalchemy import select

from app.db_models import UserAction
from tests.conftest import TestSessionLocal


def valid_employee():
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
        "id_employee": 9999,
        "a_quitte_l_entreprise": "Non",
    }


def test_create_employee_requires_api_key(client):
    response = client.post(
        "/employees",
        json=valid_employee(),
    )

    assert response.status_code == 401


def test_create_employee(client, auth_headers):
    response = client.post(
        "/employees",
        json=valid_employee(),
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["id_employee"] == 9999


def test_create_duplicate_employee_returns_409(client, auth_headers):
    response = client.post(
        "/employees",
        json=valid_employee(),
        headers=auth_headers,
    )

    assert response.status_code == 409


def test_delete_employee(client, auth_headers):
    response = client.delete(
        "/employees/9999",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["id_employee"] == 9999


def test_delete_unknown_employee_returns_404(client, auth_headers):
    response = client.delete(
        "/employees/9999",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_employee_actions_are_audited():
    with TestSessionLocal() as db:
        actions = db.scalars(
            select(UserAction)
            .where(
                UserAction.resource_type == "employee",
                UserAction.resource_id == "9999",
            )
            .order_by(UserAction.created_at)
        ).all()

    assert len(actions) == 2

    assert actions[0].action == "CREATE"
    assert actions[1].action == "DELETE"

    assert actions[0].user_id == actions[1].user_id
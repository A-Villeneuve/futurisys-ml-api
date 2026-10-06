import pytest
from pydantic import ValidationError

from app.schemas import EmployeeInput


def valid_employee_data():
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


def test_employee_input_accepts_valid_data():
    employee = EmployeeInput(**valid_employee_data())

    assert employee.age == 30
    assert employee.poste == "Consultant"
    assert employee.revenu_mensuel == 3500


def test_employee_input_rejects_age_under_18():
    data = valid_employee_data()
    data["age"] = 17

    with pytest.raises(ValidationError):
        EmployeeInput(**data)


def test_employee_input_rejects_invalid_department():
    data = valid_employee_data()
    data["departement"] = "Informatique"

    with pytest.raises(ValidationError):
        EmployeeInput(**data)


def test_employee_input_rejects_invalid_satisfaction():
    data = valid_employee_data()
    data["satisfaction_employee_equipe"] = 5

    with pytest.raises(ValidationError):
        EmployeeInput(**data)
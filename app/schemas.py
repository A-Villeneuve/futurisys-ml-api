from typing import Literal

from pydantic import BaseModel, Field


class EmployeeInput(BaseModel):
    # Profil
    age: int = Field(ge=18)
    genre: Literal["F", "M"]
    statut_marital: Literal[
        "Célibataire",
        "Divorcé(e)",
        "Marié(e)",
    ]
    distance_domicile_travail: int = Field(ge=0)

    # Poste
    departement: Literal[
        "Commercial",
        "Consulting",
        "Ressources Humaines",
    ]
    poste: Literal[
        "Assistant de Direction",
        "Cadre Commercial",
        "Consultant",
        "Directeur Technique",
        "Manager",
        "Représentant Commercial",
        "Ressources Humaines",
        "Senior Manager",
        "Tech Lead",
    ]
    niveau_hierarchique_poste: int = Field(ge=1, le=5)

    # Rémunération
    revenu_mensuel: int = Field(gt=0)
    augementation_salaire_precedente: float = Field(ge=0)
    nombre_participation_pee: int = Field(ge=0)

    # Expérience et ancienneté
    nombre_experiences_precedentes: int = Field(ge=0)
    annee_experience_totale: int = Field(ge=0)
    annees_dans_l_entreprise: int = Field(ge=0)
    annees_dans_le_poste_actuel: int = Field(ge=0)
    annees_depuis_la_derniere_promotion: int = Field(ge=0)
    annes_sous_responsable_actuel: int = Field(ge=0)

    # Satisfaction / évaluations
    satisfaction_employee_environnement: int = Field(ge=1, le=4)
    satisfaction_employee_nature_travail: int = Field(ge=1, le=4)
    satisfaction_employee_equipe: int = Field(ge=1, le=4)
    satisfaction_employee_equilibre_pro_perso: int = Field(ge=1, le=4)
    note_evaluation_precedente: int = Field(ge=1, le=4)
    note_evaluation_actuelle: int = Field(ge=1, le=4)

    # Conditions de travail
    heure_supplementaires: Literal["Non", "Oui"]
    frequence_deplacement: Literal[
        "Aucun",
        "Occasionnel",
        "Frequent",
    ]

    # Formation
    niveau_education: int = Field(ge=1, le=5)
    domaine_etude: Literal[
        "Autre",
        "Entrepreunariat",
        "Infra & Cloud",
        "Marketing",
        "Ressources Humaines",
        "Transformation Digitale",
    ]
    nb_formations_suivies: int = Field(ge=0)


class PredictionResponse(BaseModel):
    prediction_id: int
    probability: float = Field(ge=0, le=1)
    prediction: bool
    threshold: float = Field(ge=0, le=1)
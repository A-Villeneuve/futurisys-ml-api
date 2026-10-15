from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    OrdinalEncoder,
    StandardScaler,
)

from app.ml.feature_engineering import FeatureEngineer


# -------------------------------------------------------------------
# Chemins du projet
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"

SIRH_PATH = DATA_DIR / "extrait_sirh.csv"
EVAL_PATH = DATA_DIR / "extrait_eval.csv"
SONDAGE_PATH = DATA_DIR / "extrait_sondage.csv"

MODEL_PATH = MODEL_DIR / "attrition_pipeline.joblib"


# -------------------------------------------------------------------
# Chargement des données
# -------------------------------------------------------------------

def load_data():
    df_sirh = pd.read_csv(SIRH_PATH)
    df_eval = pd.read_csv(EVAL_PATH)
    df_sondage = pd.read_csv(SONDAGE_PATH)

    return df_sirh, df_eval, df_sondage


# -------------------------------------------------------------------
# Construction du dataset central
# -------------------------------------------------------------------

def build_dataset(df_sirh, df_eval, df_sondage):
    df_sirh = df_sirh.copy()
    df_eval = df_eval.copy()
    df_sondage = df_sondage.copy()

    # Reconstruction d'une clé commune
    df_eval["id_employee"] = (
        df_eval["eval_number"]
        .str.replace("E_", "", regex=False)
        .astype(int)
    )

    df_sondage = df_sondage.rename(
        columns={"code_sondage": "id_employee"}
    )

    # Vérification de l'unicité
    if not df_sirh["id_employee"].is_unique:
        raise ValueError(
            "id_employee n'est pas unique dans le fichier SIRH."
        )

    if not df_eval["id_employee"].is_unique:
        raise ValueError(
            "id_employee n'est pas unique dans le fichier d'évaluation."
        )

    if not df_sondage["id_employee"].is_unique:
        raise ValueError(
            "id_employee n'est pas unique dans le fichier de sondage."
        )

    # Vérification de la cohérence entre les trois sources
    ids_sirh = set(df_sirh["id_employee"])
    ids_eval = set(df_eval["id_employee"])
    ids_sondage = set(df_sondage["id_employee"])

    if not (ids_sirh == ids_eval == ids_sondage):
        raise ValueError(
            "Les identifiants employés ne correspondent pas "
            "entre les trois sources."
        )

    # Conversion du pourcentage en numérique
    df_eval["augementation_salaire_precedente"] = (
        df_eval["augementation_salaire_precedente"]
        .str.replace("%", "", regex=False)
        .str.strip()
        .astype(float)
    )

    # Suppression des variables inutiles / constantes
    df_sirh = df_sirh.drop(
        columns=["nombre_heures_travailless"]
    )

    df_eval = df_eval.drop(
        columns=["eval_number"]
    )

    df_sondage = df_sondage.drop(
        columns=[
            "nombre_employee_sous_responsabilite",
            "ayant_enfants",
        ]
    )

    # Jointure one-to-one
    df_central = (
        df_sirh
        .merge(
            df_eval,
            on="id_employee",
            how="left",
            validate="one_to_one",
        )
        .merge(
            df_sondage,
            on="id_employee",
            how="left",
            validate="one_to_one",
        )
    )

    return df_central


# -------------------------------------------------------------------
# Séparation X / y
# -------------------------------------------------------------------

def prepare_training_data(df):
    X = df.drop(
        columns=[
            "a_quitte_l_entreprise",
            "id_employee",
        ]
    )

    y = df["a_quitte_l_entreprise"].map(
        {
            "Non": 0,
            "Oui": 1,
        }
    )

    if y.isna().any():
        raise ValueError(
            "La cible contient une valeur différente de 'Oui' ou 'Non'."
        )

    return X, y


# -------------------------------------------------------------------
# Construction du pipeline ML
# -------------------------------------------------------------------

def build_pipeline():

    # Variables après passage dans FeatureEngineer
    variables_numeriques = [
        "age",
        "revenu_mensuel",
        "nombre_experiences_precedentes",
        "annee_experience_totale",
        "annees_dans_l_entreprise",
        "augementation_salaire_precedente",
        "nombre_participation_pee",
        "nb_formations_suivies",
        "distance_domicile_travail",
        "annees_depuis_la_derniere_promotion",
        "satisfaction_employee_environnement",
        "note_evaluation_precedente",
        "niveau_hierarchique_poste",
        "satisfaction_employee_nature_travail",
        "satisfaction_employee_equipe",
        "satisfaction_employee_equilibre_pro_perso",
        "note_evaluation_actuelle",
        "niveau_education",
        "nouvel_employe",
        "ratio_anciennete_poste",
        "ratio_anciennete_responsable",
    ]

    variables_binaires = [
        "genre",
        "heure_supplementaires",
    ]

    variable_deplacement = [
        "frequence_deplacement",
    ]

    variables_nominales = [
        "statut_marital",
        "departement",
        "poste",
        "domaine_etude",
    ]

    binary_encoder = OrdinalEncoder(
        categories=[
            ["F", "M"],
            ["Non", "Oui"],
        ],
        handle_unknown="use_encoded_value",
        unknown_value=-1,
    )

    deplacement_encoder = OrdinalEncoder(
        categories=[
            ["Aucun", "Occasionnel", "Frequent"],
        ],
        handle_unknown="use_encoded_value",
        unknown_value=-1,
    )

    onehot_encoder = OneHotEncoder(
        handle_unknown="ignore"
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                variables_numeriques,
            ),
            (
                "binary",
                binary_encoder,
                variables_binaires,
            ),
            (
                "deplacement",
                deplacement_encoder,
                variable_deplacement,
            ),
            (
                "nominal",
                onehot_encoder,
                variables_nominales,
            ),
        ],
        remainder="drop",
    )

    model = RandomForestClassifier(
        n_estimators=700,
        max_depth=8,
        min_samples_split=15,
        min_samples_leaf=4,
        max_features="log2",
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    pipeline = Pipeline(
        [
            (
                "feature_engineering",
                FeatureEngineer(),
            ),
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                model,
            ),
        ]
    )

    return pipeline


# -------------------------------------------------------------------
# Entraînement et évaluation
# -------------------------------------------------------------------

def train_and_evaluate(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("Train :", X_train.shape)
    print("Test  :", X_test.shape)

    pipeline = build_pipeline()

    print("\nEntraînement du modèle...")
    pipeline.fit(X_train, y_train)

    probability = pipeline.predict_proba(X_test)[:, 1]

    threshold = 0.446
    prediction = (probability >= threshold).astype(int)

    print(f"\nSeuil : {threshold}")

    print(
        "Accuracy :",
        round(accuracy_score(y_test, prediction), 3),
    )
    print(
        "Precision :",
        round(precision_score(y_test, prediction), 3),
    )
    print(
        "Recall :",
        round(recall_score(y_test, prediction), 3),
    )
    print(
        "F1 :",
        round(f1_score(y_test, prediction), 3),
    )
    print(
        "ROC-AUC :",
        round(roc_auc_score(y_test, probability), 3),
    )
    print(
        "PR-AUC :",
        round(average_precision_score(y_test, probability), 3),
    )

    print("\nMatrice de confusion :")
    print(confusion_matrix(y_test, prediction))

    return pipeline


# -------------------------------------------------------------------
# Sauvegarde du modèle
# -------------------------------------------------------------------

def save_model(pipeline):
    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        pipeline,
        MODEL_PATH,
    )

    print(f"\nModèle sauvegardé : {MODEL_PATH}")


# -------------------------------------------------------------------
# Exécution du script
# -------------------------------------------------------------------

if __name__ == "__main__":
    sirh, evaluation, sondage = load_data()

    df = build_dataset(
        sirh,
        evaluation,
        sondage,
    )

    print("Dataset central :", df.shape)

    X, y = prepare_training_data(df)

    print("Variables modèle :", X.shape)

    pipeline = train_and_evaluate(X, y)

    save_model(pipeline)
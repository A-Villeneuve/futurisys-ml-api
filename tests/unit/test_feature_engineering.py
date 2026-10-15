import pandas as pd

from app.ml.feature_engineering import FeatureEngineer


def test_feature_engineer_calculates_features():
    df = pd.DataFrame(
        {
            "annees_dans_l_entreprise": [4],
            "annees_dans_le_poste_actuel": [2],
            "annes_sous_responsable_actuel": [1],
        }
    )

    transformer = FeatureEngineer()

    result = transformer.fit_transform(df)

    assert result["nouvel_employe"].iloc[0] == 0
    assert result["ratio_anciennete_poste"].iloc[0] == 0.5
    assert result["ratio_anciennete_responsable"].iloc[0] == 0.25

    assert "annees_dans_le_poste_actuel" not in result.columns
    assert "annes_sous_responsable_actuel" not in result.columns


def test_feature_engineer_handles_new_employee():
    df = pd.DataFrame(
        {
            "annees_dans_l_entreprise": [0],
            "annees_dans_le_poste_actuel": [0],
            "annes_sous_responsable_actuel": [0],
        }
    )

    transformer = FeatureEngineer()

    result = transformer.fit_transform(df)

    assert result["nouvel_employe"].iloc[0] == 1
    assert result["ratio_anciennete_poste"].iloc[0] == 0
    assert result["ratio_anciennete_responsable"].iloc[0] == 0
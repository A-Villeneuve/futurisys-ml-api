import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin


class FeatureEngineer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        X["nouvel_employe"] = (
            X["annees_dans_l_entreprise"] == 0
        ).astype(int)

        X["ratio_anciennete_poste"] = np.where(
            X["annees_dans_l_entreprise"] > 0,
            X["annees_dans_le_poste_actuel"]
            / X["annees_dans_l_entreprise"],
            0
        )

        X["ratio_anciennete_responsable"] = np.where(
            X["annees_dans_l_entreprise"] > 0,
            X["annes_sous_responsable_actuel"]
            / X["annees_dans_l_entreprise"],
            0
        )

        X = X.drop(
            columns=[
                "annees_dans_le_poste_actuel",
                "annes_sous_responsable_actuel"
            ]
        )

        return X
from sqlalchemy import select

from app.database import SessionLocal
from app.db_models import Model


MODEL_NAME = "attrition_random_forest"
MODEL_VERSION = "1.0.0"
MODEL_THRESHOLD = 0.446
MODEL_PATH = "models/attrition_pipeline.joblib"


def init_model():
    with SessionLocal() as session:
        existing_model = session.scalar(
            select(Model).where(Model.version == MODEL_VERSION)
        )

        if existing_model:
            print(f"Modèle {MODEL_VERSION} déjà enregistré.")
            return

        model = Model(
            name=MODEL_NAME,
            version=MODEL_VERSION,
            threshold=MODEL_THRESHOLD,
            model_path=MODEL_PATH,
        )

        session.add(model)
        session.commit()
        session.refresh(model)

        print(
            f"Modèle enregistré : "
            f"id={model.id}, "
            f"name={model.name}, "
            f"version={model.version}"
        )


if __name__ == "__main__":
    init_model()
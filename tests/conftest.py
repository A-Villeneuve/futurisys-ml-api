import hashlib
import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.db_models import Model, User
from app.main import app


load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
TEST_API_KEY = "test-api-key"

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "La variable d'environnement TEST_DATABASE_URL n'est pas définie."
    )


test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


def override_get_db():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # On repart d'une base de test propre
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    # Données minimales nécessaires au fonctionnement de l'API
    with TestSessionLocal() as db:
        user = User(
            username="pytest_user",
            api_key_hash=hashlib.sha256(
                TEST_API_KEY.encode()
            ).hexdigest(),
            is_active=True,
        )

        model = Model(
            name="attrition_random_forest",
            version="1.0.0",
            threshold=0.446,
            model_path="models/attrition_pipeline.joblib",
        )

        db.add_all([user, model])
        db.commit()

    yield

    # Nettoyage après toute la session Pytest
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers():
    return {
        "X-API-Key": TEST_API_KEY,
    }
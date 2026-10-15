import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Charge les variables définies dans le fichier .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "La variable d'environnement DATABASE_URL n'est pas définie."
    )


# Engine = point de connexion entre SQLAlchemy et PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


#  permet de créer des sessions avec PostgreSQL
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Classe mère de nos futurs modèles SQLAlchemy
class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
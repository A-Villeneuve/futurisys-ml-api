import argparse

from app import db_models
from app.database import Base, engine


def init_database(reset: bool = False):
    if reset:
        print("Suppression des tables existantes...")
        Base.metadata.drop_all(bind=engine)

    print("Création des tables PostgreSQL...")
    Base.metadata.create_all(bind=engine)

    print("Base de données initialisée avec succès.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Supprime les tables existantes avant de les recréer.",
    )
    args = parser.parse_args()

    init_database(reset=args.reset)
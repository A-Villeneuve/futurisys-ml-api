from sqlalchemy import func, select

from app.database import SessionLocal
from app.db_models import Employee
from scripts.train_model import build_dataset, load_data


def load_employees():
    # Reconstruction du dataset central
    df_sirh, df_eval, df_sondage = load_data()

    df = build_dataset(
        df_sirh,
        df_eval,
        df_sondage,
    )

    print(f"Dataset à importer : {df.shape}")

    with SessionLocal() as session:
        # Vérifie si employees contient déjà des données
        employee_count = session.scalar(
            select(func.count()).select_from(Employee)
        )

        if employee_count > 0:
            print(
                f"Import annulé : la table employees contient déjà "
                f"{employee_count} employés."
            )
            return

        # DataFrame -> liste d'objets ORM
        employees = [
            Employee(**row)
            for row in df.to_dict(orient="records")
        ]

        session.add_all(employees)
        session.commit()

        print(f"{len(employees)} employés insérés avec succès.")


if __name__ == "__main__":
    load_employees()
import hashlib
import secrets

from sqlalchemy import select

from app.database import SessionLocal
from app.db_models import User


USERNAME = "anthony"


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()


def create_user():
    with SessionLocal() as session:
        existing_user = session.scalar(
            select(User).where(User.username == USERNAME)
        )

        if existing_user:
            print(f"L'utilisateur '{USERNAME}' existe déjà.")
            return

        api_key = secrets.token_urlsafe(32)
        api_key_hash = hash_api_key(api_key)

        user = User(
            username=USERNAME,
            api_key_hash=api_key_hash,
            is_active=True,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        print(f"Utilisateur créé : id={user.id}, username={user.username}")
        print()
        print("Clé API :")
        print(api_key)
        


if __name__ == "__main__":
    create_user()
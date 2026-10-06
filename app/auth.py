import hashlib

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.db_models import User


api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()


def get_current_user(
    api_key: str | None = Security(api_key_header),
    db: Session = Depends(get_db),
) -> User:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API manquante.",
        )

    api_key_hash = hash_api_key(api_key)

    user = db.scalar(
        select(User).where(
            User.api_key_hash == api_key_hash,
            User.is_active.is_(True),
        )
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API invalide.",
        )

    return user
FROM python:3.12-slim

WORKDIR /app

# uv permet de reproduire exactement l'environnement défini par uv.lock
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

# L'API et le modèle sont nécessaires à l'exécution
COPY app ./app
COPY models ./models

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
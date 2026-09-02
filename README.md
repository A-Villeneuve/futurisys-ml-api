# Futurisys ML API

API de déploiement d'un modèle de Machine Learning permettant de prédire le risque d'attrition des employés.

## Contexte

Ce projet a pour objectif de mettre en production un modèle de Machine Learning dans le cadre d'une mission réalisée pour l'entreprise fictive Futurisys.

Le modèle doit être accessible à travers une API, documenté, testé et intégré dans une architecture permettant de garantir la traçabilité des prédictions.

## Objectifs

Le projet doit permettre de :

- exposer le modèle de Machine Learning via une API FastAPI ;
- valider les données entrantes avec Pydantic ;
- enregistrer les données utilisées pour les prédictions dans une base PostgreSQL ;
- enregistrer les résultats des prédictions afin d'assurer leur traçabilité ;
- mettre en place des tests automatisés avec Pytest ;
- automatiser les contrôles et le déploiement avec un pipeline CI/CD ;
- documenter l'installation, l'utilisation et l'architecture du projet.

## Architecture du projet

```text
futurisys-ml-api/
├── app/          # Code de l'API
├── models/       # Modèle de Machine Learning sérialisé
├── tests/        # Tests unitaires et fonctionnels
├── scripts/      # Scripts utilitaires et base de données
├── data/         # Données utilisées par le projet
├── docs/         # Documentation complémentaire, schéma etc...
├── main.py
├── pyproject.toml
└── README.md
```

## Installation

Le projet utilise Python 3.12 et uv pour la gestion de l’environnement et des dépendances. 
Pour créer un environnement virtuel : 
```bash
 uv venv
  ```
Pour l'activer : 
```bash 
source .venv/bin/activate
 ```
Pour installer les dépendances du projets : 
```bash
 uv sync
  ```

## Workflow git

Le projet utilise trois niveaux principaux de branches:
```text
main
└── developpement
    └── feature/*
```

* `main` contient les versions stables du projet ;
* `developpement` contient les fonctionnalités validées avant passage en production ;
* `feature/*` est utilisé pour développer une fonctionnalité spécifique.
Les fonctionnalités sont développées sur une branche dédiée puis intégrées dans developpement via une Pull Request.

## Convention de commits
```text
feat: nouvelle fonctionnalité
fix: correction d'un bug
test: ajout ou modification de tests
docs: documentation
ci: modification de la CI/CD
tache : configuration ou maintenance du projet
```

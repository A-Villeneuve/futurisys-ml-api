# Futurisys ML API

API REST de prédiction du risque d'attrition des employés, développée avec FastAPI et intégrant un modèle de Machine Learning.

Le projet comprend une base de données PostgreSQL, un système d'authentification par clé API, des tests automatisés et un déploiement local avec Docker Compose.

**Version du projet :** `v1.0.1`

**Dépôt GitHub :** [Futurisys ML API](https://github.com/A-Villeneuve/futurisys-ml-api)

---

## 1. Contexte et objectifs

Futurisys est une entreprise fictive souhaitant anticiper les départs de ses collaborateurs.

L'objectif du projet est d'industrialiser un modèle de Machine Learning capable d'estimer la probabilité de départ d'un salarié.

L'application permet notamment de :

- exposer le modèle de prédiction à travers une API REST ;
- valider les données entrantes avec Pydantic ;
- authentifier les utilisateurs à l'aide d'une clé API ;
- enregistrer les employés dans une base PostgreSQL ;
- conserver les demandes et les résultats des prédictions ;
- assurer la traçabilité des actions réalisées ;
- automatiser les tests et les contrôles de qualité ;
- déployer localement l'application avec Docker Compose.

## 2. Architecture technique

L'application repose sur les composants suivants :

| Composant | Technologie | Rôle |
|---|---|---|
| API REST | FastAPI | Exposition des fonctionnalités |
| Validation | Pydantic | Validation des données entrantes |
| Machine Learning | Scikit-learn | Prédiction du risque d'attrition |
| Base de données | PostgreSQL 16 | Stockage et traçabilité |
| ORM | SQLAlchemy | Interaction avec la base |
| Authentification | Clé API | Contrôle des accès |
| Tests | Pytest | Tests automatisés |
| Couverture | pytest-cov | Mesure de la couverture |
| Conteneurisation | Docker | Construction de l'application |
| Orchestration | Docker Compose | Démarrage des services |
| CI | GitHub Actions | Tests et validation du déploiement |
| Dépendances | uv | Gestion de l'environnement Python |

### Fonctionnement général

```text
                  Utilisateur
                      |
                      v
                API FastAPI
                      |
             Authentification
                      |
              Validation Pydantic
                      |
              Modèle ML chargé
                      |
                 Prédiction
                      |
                      v
                 PostgreSQL
                      |
           Historique et traçabilité
```

L'API utilise un modèle de Machine Learning sérialisé et chargé au démarrage.

Les demandes de prédiction et leurs résultats sont enregistrés en base afin d'assurer leur traçabilité.

L'architecture sépare les responsabilités :

- **FastAPI** gère les requêtes HTTP et les réponses.
- **Pydantic** valide les données entrantes.
- **Scikit-learn** réalise les prédictions.
- **SQLAlchemy** assure les interactions avec PostgreSQL.
- **PostgreSQL** conserve les données et les historiques.
- **Docker Compose** orchestre les services nécessaires.

## 3. Modèle de Machine Learning

Le modèle utilisé est un Random Forest entraîné sur les données RH de Futurisys.

Il s'appuie sur 27 variables décrivant notamment les caractéristiques professionnelles et les conditions de travail des employés.

Le pipeline de prédiction comprend :

1. La préparation des variables.
2. Le prétraitement des données.
3. L'application du modèle Random Forest.
4. Le calcul de la probabilité de départ.
5. L'application d'un seuil de classification.

### Performances

Les performances suivantes ont été obtenues sur le jeu de test :

| Métrique | Résultat |
|---|---:|
| Accuracy | 77,9 % |
| Precision | 39,0 % |
| Recall | 68,1 % |
| F1-score | 49,6 % |
| ROC-AUC | 0,786 |
| PR-AUC | 0,412 |

Le seuil de classification retenu est de **0,446**.

Une probabilité supérieure ou égale à ce seuil conduit à une prédiction positive du risque de départ.

Le rappel est particulièrement important dans ce contexte : il mesure la proportion des départs effectivement détectés par le modèle.

Les prédictions restent des estimations statistiques et ne constituent pas des certitudes sur le comportement individuel des employés.

### Modèle sérialisé

Le modèle entraîné est disponible dans :

```text
models/attrition_pipeline.joblib
```

Ce fichier est inclus dans le dépôt GitHub et dans l'image Docker.

Il permet d'exécuter les prédictions sans devoir réentraîner le modèle à chaque démarrage de l'application.

## 4. Organisation du dépôt

```text
futurisys-ml-api/
|
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|
|-- app/
|   |-- auth.py
|   |-- database.py
|   |-- db_models.py
|   |-- main.py
|   |-- schemas.py
|   `-- ml/
|       |-- __init__.py
|       |-- feature_engineering.py
|       `-- predictor.py
|
|-- models/
|   `-- attrition_pipeline.joblib
|
|-- scripts/
|   |-- init_db.py
|   |-- init_model.py
|   |-- load_data.py
|   |-- create_user.py
|   `-- train_model.py
|
|-- tests/
|   |-- conftest.py
|   |-- integration/
|   `-- unit/
|
|-- data/
|   |-- extrait_sirh.csv
|   |-- extrait_eval.csv
|   `-- extrait_sondage.csv
|
|-- docs/
|   `-- diagERD_P5.png
|
|-- .dockerignore
|-- .env.example
|-- .gitignore
|-- Dockerfile
|-- compose.yaml
|-- pyproject.toml
|-- uv.lock
`-- README.md
```

### Données du projet

Le répertoire `data/` contient les trois fichiers CSV fictifs fournis dans le cadre du projet pédagogique.

Ces fichiers sont **versionnés dans le dépôt GitHub** et sont donc automatiquement disponibles après le clonage du projet.

Ils permettent notamment de :

- reproduire l'entraînement du modèle ;
- préparer les données RH ;
- importer les employés dans PostgreSQL.

Les fichiers CSV ne sont toutefois **pas intégrés à l'image Docker**.

Cette séparation permet de conserver une image applicative indépendante des données sources.

Pour importer les employés, les fichiers sont montés temporairement dans un conteneur Docker.

## 5. Prérequis

Pour exécuter le projet localement, les outils suivants sont nécessaires :

- Git ;
- Docker et Docker Compose ;
- Python 3.12 pour une exécution hors Docker ;
- uv pour la gestion des dépendances Python.

Docker Compose permet de démarrer l'application sans installer manuellement PostgreSQL sur la machine hôte.

## 6. Installation

### 6.1. Récupérer le dépôt

Avec SSH :

```bash
git clone git@github.com:A-Villeneuve/futurisys-ml-api.git
cd futurisys-ml-api
```

Il est également possible de cloner le dépôt avec HTTPS :

```bash
git clone https://github.com/A-Villeneuve/futurisys-ml-api.git
cd futurisys-ml-api
```

### 6.2. Configurer les variables d'environnement

Créer un fichier `.env` à partir du modèle fourni :

```bash
cp .env.example .env
```

Le fichier `.env.example` présente les variables nécessaires à la configuration.

Pour le déploiement Docker Compose, renseigner notamment :

```dotenv
DOCKER_DB_PASSWORD=remplacer_par_un_mot_de_passe_securise
```

Un mot de passe peut être généré avec :

```bash
openssl rand -hex 24
```

La valeur générée doit être copiée dans le fichier `.env`.

Le fichier `.env` contient des informations sensibles et ne doit jamais être ajouté au dépôt Git.

### 6.3. Installer les dépendances Python

Cette étape est utile pour le développement et l'exécution des tests en dehors de Docker.

```bash
uv sync --dev
```

Les dépendances sont définies dans `pyproject.toml` et verrouillées dans `uv.lock`.

Pour exécuter les commandes Python dans l'environnement du projet, il est possible d'utiliser `uv run`.

## 7. Déploiement local avec Docker Compose

### 7.1. Démarrer les services

Depuis la racine du projet :

```bash
docker compose up -d --build
```

Cette commande :

1. Construit l'image de l'application.
2. Démarre PostgreSQL.
3. Attend que la base soit disponible.
4. Initialise les tables.
5. Enregistre le modèle de Machine Learning.
6. Démarre l'API FastAPI.

### 7.2. Vérifier les conteneurs

```bash
docker compose ps -a
```

Les services attendus sont :

| Service | Fonction |
|---|---|
| `db` | Base de données PostgreSQL |
| `init` | Initialisation de la base et du modèle |
| `api` | Application FastAPI |

Le conteneur `init` doit normalement se terminer avec le code `0` après son exécution.

### 7.3. Vérifier l'état de l'API

```bash
curl http://localhost:8000/health
```

Réponse attendue :

```json
{
  "status": "healthy",
  "database": "connected",
  "model": "loaded"
}
```

Cette réponse indique que :

- l'API répond ;
- la connexion à PostgreSQL fonctionne ;
- le modèle de Machine Learning est chargé.

### 7.4. Accéder à la documentation interactive

Une fois l'application démarrée, la documentation Swagger est disponible à l'adresse :

http://localhost:8000/docs

La spécification OpenAPI est accessible à l'adresse :

http://localhost:8000/openapi.json

Swagger permet de consulter les endpoints, leurs paramètres, les schémas Pydantic et les réponses attendues.

## 8. Initialisation des données

### 8.1. Structure de la base

L'application utilise six tables principales :

| Table | Rôle |
|---|---|
| `employees` | Informations relatives aux employés |
| `prediction_requests` | Historique des demandes de prédiction |
| `prediction_results` | Résultats produits par le modèle |
| `models` | Informations sur les modèles disponibles |
| `users` | Utilisateurs autorisés |
| `user_actions` | Traçabilité des actions |

Le schéma relationnel est disponible dans :

```text
docs/diagERD_P5.png
```

### 8.2. Importer les employés

Les données sources sont directement incluses dans le dépôt GitHub.

Après le clonage du projet, les trois fichiers suivants sont déjà présents :

```text
data/
|-- extrait_sirh.csv
|-- extrait_eval.csv
`-- extrait_sondage.csv
```

**Aucun téléchargement supplémentaire n'est nécessaire.**

L'importation des employés dans PostgreSQL est une opération distincte de l'initialisation des tables et du modèle.

Après avoir démarré l'application avec Docker Compose, exécuter depuis la racine du projet :

```bash
docker compose run --rm --no-deps \
  -v "$(pwd)/data:/app/data:ro" \
  api uv run python -m scripts.load_data
```

Cette commande :

1. Crée un conteneur temporaire à partir de l'image de l'API.
2. Monte le répertoire local `data/` dans le conteneur.
3. Rend les fichiers CSV accessibles en lecture seule.
4. Exécute le script d'importation.
5. Enregistre les employés dans PostgreSQL.
6. Supprime le conteneur temporaire après son exécution.

L'importation porte sur **1 470 employés**.

Le script vérifie si des employés sont déjà présents dans la base avant de procéder à l'importation.

Cette opération n'est donc pas nécessaire à chaque redémarrage de l'application.

### 8.3. Vérifier les données

```bash
docker compose exec db \
  psql -U futurisys_api -d futurisys \
  -c "SELECT COUNT(*) FROM employees;"
```

Après une importation réussie, le résultat attendu est :

```text
1470
```

## 9. Authentification et utilisation de l'API

### 9.1. Créer un utilisateur

L'API utilise une authentification par clé API.

Pour créer l'utilisateur prévu par le script d'initialisation :

```bash
docker compose exec api \
  uv run python -m scripts.create_user
```

Lors de la création, une clé API est générée.

Cette clé doit être conservée dans un emplacement sécurisé.

L'application ne stocke pas la clé en clair dans PostgreSQL : elle conserve son empreinte SHA-256.

Le script actuel crée un utilisateur prédéfini. Si cet utilisateur existe déjà, il ne génère pas une nouvelle clé.

### 9.2. Authentifier une requête

Les endpoints protégés nécessitent un en-tête HTTP :

```text
X-API-Key: <votre_cle_api>
```

La clé peut être renseignée dans l'interface Swagger pour tester les opérations protégées.

Ne jamais publier une véritable clé API dans le dépôt, dans un exemple de requête ou dans les logs.

### 9.3. Principaux endpoints

| Méthode | Endpoint | Fonction |
|---|---|---|
| GET | `/health` | Vérifier l'état de l'application |
| POST | `/employees` | Créer un employé |
| DELETE | `/employees/{employee_id}` | Supprimer un employé |
| POST | `/predict` | Calculer une prédiction d'attrition |

Les schémas de requête, les champs obligatoires et les réponses sont décrits dans Swagger.

### 9.4. Exemple de réponse de prédiction

Une prédiction renvoie notamment :

```json
{
  "prediction_id": 1,
  "probability": 0.5700421405489682,
  "prediction": true,
  "threshold": 0.446
}
```

Interprétation :

- `prediction_id` : identifiant de la prédiction enregistrée ;
- `probability` : probabilité estimée de départ ;
- `prediction` : résultat de la classification ;
- `threshold` : seuil appliqué à la probabilité.

Dans cet exemple, la probabilité estimée est d'environ 57 %, supérieure au seuil de 44,6 %.

Le modèle classe donc l'employé dans la catégorie présentant un risque de départ.

Les résultats sont enregistrés dans PostgreSQL afin de conserver un historique des prédictions réalisées.

## 10. Tests automatisés

Le projet utilise Pytest pour vérifier le fonctionnement de l'application.

Les tests couvrent notamment :

- la validation des données ;
- les transformations de variables ;
- le fonctionnement des endpoints ;
- les interactions avec la base de données ;
- les opérations liées aux employés ;
- les prédictions.

Une base PostgreSQL de test distincte est utilisée afin de ne pas modifier les données de l'application.

### 10.1. Exécuter les tests

Pour exécuter les tests hors Docker, configurer préalablement `TEST_DATABASE_URL` vers une base PostgreSQL de test accessible.

Puis lancer :

```bash
uv run pytest
```

### 10.2. Mesurer la couverture

```bash
uv run pytest \
  --cov=app \
  --cov-report=term-missing \
  --cov-fail-under=90
```

Résultats obtenus lors de la validation du projet :

| Indicateur | Résultat |
|---|---:|
| Tests réussis | 18 |
| Couverture du code applicatif | 92,81 % |
| Seuil minimal exigé | 90 % |

La couverture mesure la proportion du code exécutée pendant les tests. Elle ne garantit pas, à elle seule, l'absence de défauts.

## 11. Intégration continue et validation du déploiement

Le workflow GitHub Actions est défini dans :

```text
.github/workflows/ci.yml
```

Il est déclenché lors :

- des pushs vers `developpement` et `main` ;
- des Pull Requests vers `developpement` et `main`.

### Job `tests`

Ce job :

1. Prépare un environnement Ubuntu.
2. Démarre un service PostgreSQL de test.
3. Installe Python 3.12 et les dépendances.
4. Exécute les tests Pytest.
5. Vérifie que la couverture atteint au moins 90 %.

### Job `docker`

Ce job démarre uniquement si les tests réussissent.

Il :

1. Construit les images Docker.
2. Démarre l'application avec Docker Compose.
3. Vérifie la réponse de `/health`.
4. Contrôle la connexion à PostgreSQL.
5. Vérifie le chargement du modèle.
6. Affiche les logs en cas d'échec.
7. Arrête et supprime les conteneurs de test.

Les deux jobs ont été validés avec succès sur GitHub Actions.

**Périmètre du pipeline :** il s'agit d'une intégration continue accompagnée d'un test automatisé de déploiement.

Le workflow ne réalise pas de déploiement permanent sur un serveur de production.

## 12. Persistance des données

Docker Compose utilise un volume nommé `postgres_data` pour conserver les données PostgreSQL.

Les données sont conservées après un arrêt classique des conteneurs :

```bash
docker compose down
```

Pour redémarrer :

```bash
docker compose up -d
```

Attention : la commande suivante supprime également les volumes associés au projet et peut donc entraîner la perte des données stockées :

```bash
docker compose down -v
```

Elle doit être réservée aux situations où une réinitialisation des données est souhaitée.

## 13. Workflow Git

Le projet repose sur trois niveaux de branches :

```text
main
  |
  `-- developpement
        |
        `-- feature/*
```

- `main` : branche destinée aux versions stables ;
- `developpement` : intégration des fonctionnalités validées ;
- `feature/*` : développement d'une fonctionnalité spécifique.

Des branches `docs/*` sont également utilisées pour les modifications documentaires.

Les fonctionnalités sont intégrées via des Pull Requests.

Les contrôles GitHub Actions permettent de vérifier les modifications avant leur fusion.

### Convention de commits

```text
feat: nouvelle fonctionnalité
fix: correction d'un bug
test: ajout ou modification de tests
docs: documentation
ci: modification de la CI
chore: configuration ou maintenance
```

## 14. Sécurité et limites

Plusieurs mesures sont mises en place :

- validation des données entrantes avec Pydantic ;
- authentification par clé API ;
- stockage des empreintes des clés API plutôt que des clés en clair ;
- séparation des bases applicative et de test ;
- exclusion des secrets du dépôt Git ;
- accès au port de l'API limité à l'interface locale dans Docker Compose ;
- utilisation d'un mot de passe PostgreSQL spécifique aux tests CI.

### Limites du projet

Le déploiement est conçu pour une démonstration et une utilisation locale.

Il ne comprend pas :

- d'hébergement de production permanent ;
- de terminaison HTTPS ;
- de système complet de gestion des rôles ;
- de rotation automatisée des clés API ;
- de supervision de production.

Ces fonctionnalités constitueraient des évolutions possibles avant une exploitation réelle.

## 15. Arrêt de l'application

Pour arrêter les services sans supprimer les données :

```bash
docker compose down
```

Pour consulter les logs :

```bash
docker compose logs
```

Pour suivre les logs de l'API :

```bash
docker compose logs -f api
```

## 16. Dépôt GitHub et version du projet

Le code source de Futurisys ML API est hébergé sur GitHub.

**Dépôt GitHub :**

[https://github.com/A-Villeneuve/futurisys-ml-api](https://github.com/A-Villeneuve/futurisys-ml-api)

**Version finale du projet :** `v1.0.1`

**Version stable précédente :** `v1.0.0`

### Historique et traçabilité du développement

Le dépôt GitHub permet de consulter :

- l'historique des commits ;
- les différentes branches de développement ;
- les Pull Requests et leurs validations ;
- les résultats des workflows GitHub Actions ;
- les versions identifiées par des tags Git.

Les fonctionnalités ont été développées sur des branches dédiées, puis intégrées dans `developpement` avant leur fusion dans `main`.

### Version livrée

La version `v1.0.1` correspond à la version finale du projet remise dans le cadre de la formation.

Elle comprend :

- le code source de l'API FastAPI ;
- le modèle de Machine Learning sérialisé ;
- les scripts de gestion de la base PostgreSQL ;
- les données fictives du projet ;
- les tests automatisés ;
- la configuration Docker Compose ;
- le workflow GitHub Actions ;
- la documentation technique.

L'archive ZIP de livraison est générée à partir du tag Git `v1.0.1`, afin de garantir la correspondance entre les fichiers remis et la version publiée.

Le dépôt GitHub constitue également une preuve du travail de versionnement et d'intégration continue réalisé tout au long du projet.

---

Projet réalisé dans le cadre d'un parcours de formation Data Scientist.
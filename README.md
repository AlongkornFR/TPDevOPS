# TP DevOps — API Hybride SQL / NoSQL

Projet pédagogique démontrant une architecture conteneurisée avec Docker Compose, orchestrant une API FastAPI connectée simultanément à une base SQL (MySQL) et une base NoSQL (MongoDB), accompagnées de leurs interfaces d'administration.

### Services

| Service | Image | Port | Rôle |
|---------|-------|------|------|
| `api` | FastAPI (build local) | 8000 | API REST hybride |
| `db_mongo` | MongoDB (build local) | — | Base NoSQL (articles de blog) |
| `db_mysql` | mysql:8.0 | — | Base SQL (utilisateurs) |
| `admin_mongo` | mongo-express | 8081 | Interface admin MongoDB |
| `admin_mysql` | adminer | 8082 | Interface admin MySQL |

## Prérequis

- Docker
- Docker Compose
- Port libres : `8000`, `8081`, `8082`

## Installation

1. Cloner le dépôt :
   ```bash
   git clone <url-du-repo>
   cd TPDevOPS
   ```

2. Créer le fichier `.env` à partir du modèle :
   ```bash
   cp .env.exemple .env
   ```

3. Adapter les valeurs dans `.env` si nécessaire (mots de passe, noms de bases).

## Lancement

```bash
docker compose up -d --build
```

Les bases s'initialisent automatiquement :
- MongoDB → 5 articles insérés dans `blog_db.posts`
- MySQL → 4 utilisateurs insérés dans la table `utilisateurs`

L'API ne démarre qu'une fois les deux bases **healthy** (healthchecks métier).

## Endpoints API

Base URL : `http://localhost:8000`

| Méthode | Route | Description |
|---------|-------|-------------|
| `GET` | `/posts` | Liste des articles (MongoDB) |
| `GET` | `/users` | Liste des utilisateurs (MySQL) |
| `GET` | `/health` | État de l'API et des bases |

### Exemple

```bash
curl http://localhost:8000/health
```

Réponse attendue :
```json
{ "status": "OK", "details": { "mongo": true, "mysql": true } }
```

## Interfaces d'administration

- **mongo-express** : http://localhost:8081 — exploration MongoDB
- **adminer** : http://localhost:8082 — exploration MySQL
  - Système : `MySQL`
  - Serveur : `db_mysql`
  - Identifiants : voir `.env`

## Variables d'environnement

Voir `.env.exemple` pour la liste complète :

- `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`
- `MONGO_INITDB_ROOT_USERNAME`, `MONGO_INITDB_ROOT_PASSWORD`, `MONGO_DB`
- `MONGO_URL`, `MYSQL_URL`

## Healthchecks

Tous les services déclarent un healthcheck :

- **MongoDB** : vérifie que `blog_db.posts` contient bien 5 documents.
- **MySQL** : vérifie que la table `utilisateurs` contient 4 lignes.
- **API** : interroge son propre endpoint `/health` qui ping les deux bases.

L'API utilise `depends_on` avec `condition: service_healthy` : elle ne démarre qu'après validation des bases.

## Structure du projet

```
TPDevOPS/
├── api/                  # Application FastAPI
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── mongo/                # Initialisation MongoDB
│   ├── Dockerfile
│   └── init.js
├── mysql/                # Initialisation MySQL
│   └── init.sql
├── docker-compose.yml
├── .env.exemple
└── .gitignore
```

## Arrêt et nettoyage

```bash
# Arrêter les conteneurs
docker compose down

# Arrêter + supprimer les volumes (perte des données)
docker compose down -v
```

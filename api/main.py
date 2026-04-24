import os
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import pymysql

app = FastAPI(title="API Hybride SQL/NoSQL")

# Récupération des variables d'environnement (avec des valeurs par défaut pour le dev local)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://admin_mongo:mdp_mongo@db_mongo:27017/")

MYSQL_HOST = os.getenv("MYSQL_HOST", "db_mysql")
MYSQL_USER = os.getenv("MYSQL_USER", "mon_utilisateur")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "mon_mot_de_passe")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "ma_base_hybride")

# --- Connexion MongoDB (Asynchrone via Motor) ---
mongo_client = AsyncIOMotorClient(MONGO_URL)
mongo_db = mongo_client.blog_db

# --- Fonction de connexion MySQL (Synchrone via PyMySQL) ---
def get_mysql_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        cursorclass=pymysql.cursors.DictCursor # Pour que les résultats soient des dictionnaires
    )


@app.get("/posts")
async def get_posts():
    """Retourne les articles depuis MongoDB"""
    try:
        # On exclut l'ObjectId "_id" qui n'est pas sérialisable en JSON par défaut
        cursor = mongo_db.posts.find({}, {"_id": 0})
        posts = await cursor.to_list(length=100)
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur MongoDB: {str(e)}")

@app.get("/users")
def get_users():
    """Retourne les utilisateurs depuis MySQL"""
    try:
        conn = get_mysql_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, pseudo, email FROM utilisateurs")
            users = cursor.fetchall()
        conn.close()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur MySQL: {str(e)}")


@app.get("/health")
async def healthcheck():
    """
    Vérifie la santé de l'API.
    Statut 'OK' UNIQUEMENT si MongoDB ET MySQL répondent correctement.
    """
    status = {"mongo": False, "mysql": False}

    # Test MongoDB : On envoie un 'ping' au serveur
    try:
        await mongo_client.admin.command('ping')
        status["mongo"] = True
    except Exception:
        pass

    # Test MySQL : On tente une connexion simple
    try:
        conn = get_mysql_connection()
        conn.ping(reconnect=False)
        conn.close()
        status["mysql"] = True
    except Exception:
        pass

    # Validation finale
    if status["mongo"] and status["mysql"]:
        return {"status": "OK", "details": status}
    else:
        # Si une des bases est injoignable, on renvoie une erreur 503 (Service Unavailable)
        raise HTTPException(
            status_code=503, 
            detail={"status": "ERROR", "details": status}
        )
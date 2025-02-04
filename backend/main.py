import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import time
import random

time.sleep(2)

# Initialiser FastAPI
app = FastAPI()

##### Configuration CORS
# Obligé SINON ça fonctionne pas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permettre l'accès à tout le monde
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#####

# Connexion à la base de données PostgreSQL
db_connection = psycopg2.connect(
    host="database",  # Nom du service dans docker-compose
    user="user",
    password="password",
    dbname="tournament_db"  # Nom de la DB définie dans docker-compose
)

cursor = db_connection.cursor()

# Modèles Pydantic pour les données

class Joueur(BaseModel):
    nom: str
    tournoi_nom: str

class Tournoi(BaseModel):
    nom: str

class Match(BaseModel):
    tournoi_id: int
    joueur1_id: int
    joueur2_id: int
    phase: str
    score_joueur1: int = 0
    score_joueur2: int = 0
    gagnant_id: int = None


import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fonction pour créer un tournoi dans la base de données
def create_tournoi_in_db(tournoi: Tournoi):
    try:
        cursor.execute(
            "INSERT INTO tournois (nom) VALUES (%s) RETURNING id;",
            (tournoi.nom,)
        )
        tournoi_id = cursor.fetchone()[0]
        db_connection.commit()
        return tournoi_id
    except Exception as e:
        db_connection.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Fonction pour récupérer tous les tournois
def get_all_tournois():
    try:
        cursor.execute("SELECT id, nom FROM tournois;")
        tournois = cursor.fetchall()
        return [{"id": tournoi[0], "nom": tournoi[1]} for tournoi in tournois]
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Fonction pour créer un joueur dans la base de données
def create_joueur_in_db(joueur: Joueur):
    try:
        # Fetch the tournament ID based on the tournament name
        cursor.execute(
            "SELECT id FROM tournois WHERE nom = %s;",
            (joueur.tournoi_nom,)
        )
        tournoi = cursor.fetchone()
        if not tournoi:
            raise HTTPException(status_code=404, detail="Tournoi not found")
        
        tournoi_id = tournoi[0]

        cursor.execute(
            "INSERT INTO joueurs (nom, tournoi_id) VALUES (%s, %s) RETURNING id;",
            (joueur.nom, tournoi_id)
        )
        joueur_id = cursor.fetchone()[0]
        db_connection.commit()
        return joueur_id
    except Exception as e:
        db_connection.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Fonction pour récupérer les joueurs d'un tournoi
def get_joueurs_by_tournoi_id(tournoi_id: int):
    try:
        cursor.execute(
            "SELECT id, nom FROM joueurs WHERE tournoi_id = %s;",
            (tournoi_id,)
        )
        joueurs = cursor.fetchall()
        return [{"id": joueur[0], "nom": joueur[1]} for joueur in joueurs]
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Fonction pour récupérer l'id d'un tournoi par son nom
def get_tournoi_id_by_name(nom: str):
    try:
        cursor.execute(
            "SELECT id FROM tournois WHERE nom = %s;",
            (nom,)
        )
        tournoi = cursor.fetchone()
        if tournoi:
            return {"id": tournoi[0]}
        else:
            raise HTTPException(status_code=404, detail="Tournoi not found")
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
def get_tournoi_by_id(tournoi_id: int):
    try:
        cursor.execute(
            f"SELECT * FROM tournois WHERE id = {tournoi_id};"
        )
        tournoi = cursor.fetchone()
        if tournoi:
            return tournoi
        else:
            raise HTTPException(status_code=404, detail="Tournoi not found")
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
def delete_tournoi_in_db(tournoi_id: int):
    try:
        tournoi = get_tournoi_by_id(tournoi_id)

    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    if tournoi:
        try:
            cursor.execute(
                f"DELETE FROM tournois WHERE id = {tournoi_id};"
            )
            return True
        
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
    else:
        return False

# Route pour créer un tournoi
@app.post("/tournois/")
def create_tournoi(tournoi: Tournoi):
    tournoi_id = create_tournoi_in_db(tournoi)
    return {"id": tournoi_id, "nom": tournoi.nom}

# Route pour récupérer tous les tournois
@app.get("/tournois/")
def list_tournois():
    tournois = get_all_tournois()
    return tournois

# Route pour inscrire un joueur à un tournoi
@app.post("/joueurs/")
def create_joueur(joueur: Joueur):
    joueur_id = create_joueur_in_db(joueur)
    return {"id": joueur_id, "nom": joueur.nom, "tournoi_nom": joueur.tournoi_nom}

# Route pour récupérer les joueurs d'un tournoi spécifique
@app.get("/tournois/{tournoi_id}/joueurs/")
def get_joueurs(tournoi_id: int):
    joueurs = get_joueurs_by_tournoi_id(tournoi_id)
    return joueurs

# Route pour récupérer l'id d'un tournoi par son nom
@app.get("/tournois/nom/{nom}/id/")
def get_tournoi_id(nom: str):
    tournoi_id = get_tournoi_id_by_name(nom)
    return tournoi_id

@app.delete("/tournois/{tournoi_id}")
def delete_tournoi(tournoi_id: int):
    delete_tournoi_in_db(tournoi_id)
    return
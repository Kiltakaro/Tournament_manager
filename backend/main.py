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



# Route pour créer un tournoi
@app.post("/tournois/")
def create_tournoi(tournoi: Tournoi):
    tournoi_id = create_tournoi_in_db(tournoi)
    return {"nom": tournoi.nom}


# Fonction pour créer un tournoi dans la base de données
def create_tournoi_in_db(tournoi: Tournoi):
    try:
        cursor.execute(
            "INSERT INTO tournois (nom) VALUES (%s);",
            (tournoi.nom)
        )
        db_connection.commit()
        
    except Exception as e:
        db_connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
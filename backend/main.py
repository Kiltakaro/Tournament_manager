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
    
def create_match_in_db(match: Match):
    try:
        # Récupérer l'ID du tournoi
        cursor.execute(
            "SELECT id FROM tournois WHERE nom = %s;",
            (match.tournoi_nom,)
        )
        tournoi = cursor.fetchone()
        if not tournoi:
            raise HTTPException(status_code=404, detail="Tournoi not found")
        tournoi_id = tournoi[0]

        # Récupérer les IDs des joueurs
        cursor.execute(
            "SELECT id FROM joueurs WHERE nom = %s AND tournoi_id = %s;",
            (match.joueur1_nom, tournoi_id)
        )
        joueur1 = cursor.fetchone()
        if not joueur1:
            raise HTTPException(status_code=404, detail="Joueur 1 not found")

        cursor.execute(
            "SELECT id FROM joueurs WHERE nom = %s AND tournoi_id = %s;",
            (match.joueur2_nom, tournoi_id)
        )
        joueur2 = cursor.fetchone()
        if not joueur2:
            raise HTTPException(status_code=404, detail="Joueur 2 not found")

        # Insérer le match
        cursor.execute(
            "INSERT INTO matchs (tournoi_id, joueur1_id, joueur2_id, phase) VALUES (%s, %s, %s, %s) RETURNING id;",
            (tournoi_id, joueur1[0], joueur2[0], match.phase)
        )
        match_id = cursor.fetchone()[0]
        db_connection.commit()
        return match_id
    except Exception as e:
        db_connection.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

def get_matchs_by_tournoi(nom: str):
    try:
        cursor.execute(
            "SELECT id FROM tournois WHERE nom = %s;",
            (nom,)
        )
        tournoi = cursor.fetchone()
        if not tournoi:
            raise HTTPException(status_code=404, detail="Tournoi not found")
        
        tournoi_id = tournoi[0]
        
        cursor.execute(
            "SELECT id, joueur1_id, joueur2_id, phase, score_joueur1, score_joueur2 FROM matchs WHERE tournoi_id = %s;",
            (tournoi_id,)
        )
        matchs = cursor.fetchall()
        
        results = []
        for match in matchs:
            cursor.execute("SELECT nom FROM joueurs WHERE id = %s;", (match[1],))
            joueur1 = cursor.fetchone()[0]

            cursor.execute("SELECT nom FROM joueurs WHERE id = %s;", (match[2],))
            joueur2 = cursor.fetchone()[0]

            results.append({
                "id": match[0],
                "joueur1_nom": joueur1,
                "joueur2_nom": joueur2,
                "phase": match[3],
                "score_joueur1": match[4],
                "score_joueur2": match[5]
            })
        
        return results
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
def update_match_score(match_id: int, update: Match):
    try:
        cursor.execute(
            "UPDATE matchs SET score_joueur1 = %s, score_joueur2 = %s WHERE id = %s RETURNING joueur1_id, joueur2_id;",
            (update.score_joueur1, update.score_joueur2, match_id)
        )
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Match not found")

        # Déterminer le gagnant
        gagnant_id = result[0] if update.score_joueur1 > update.score_joueur2 else result[1]
        cursor.execute(
            "UPDATE matchs SET gagnant_id = %s WHERE id = %s;",
            (gagnant_id, match_id)
        )
        db_connection.commit()
        return {"match_id": match_id, "gagnant_id": gagnant_id}
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

@app.post("/matchs/")
def create_match(match: Match):
    match_id = create_match_in_db(match)
    return {"id": match_id, "tournoi_nom": match.tournoi_nom, "joueur1_nom": match.joueur1_nom, "joueur2_nom": match.joueur2_nom, "phase": match.phase}

@app.get("/tournois/{nom}/matchs/")
def get_matchs(nom: str):
    matchs = get_matchs_by_tournoi(nom)
    return matchs

@app.put("/matchs/{match_id}/score/")
def update_score(match_id: int, update: Match):
    return update_match_score(match_id, update)


@app.delete("/tournois/{tournoi_id}")
def delete_tournoi(tournoi_id: int):
    delete_tournoi_in_db(tournoi_id)
    return
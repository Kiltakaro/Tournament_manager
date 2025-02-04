from pydantic import BaseModel

class TournoiCreate(BaseModel):
    nom: str

class JoueurCreate(BaseModel):
    nom: str
    tournoi_id: int

class MatchCreate(BaseModel):
    tournoi_id: int
    joueur1_id: int
    joueur2_id: int
    phase: str

class MatchScoreUpdate(BaseModel):
    match_id: int
    score_joueur1: int
    score_joueur2: int

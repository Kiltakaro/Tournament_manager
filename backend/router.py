from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import create_tournoi, create_joueur, create_match, update_match_score
from schemas import TournoiCreate, JoueurCreate, MatchCreate, MatchScoreUpdate
from models import Match

router = APIRouter()

@router.post("/tournoi/")
def create_tournoi_route(tournoi: TournoiCreate, db: Session = Depends(get_db)):
    return create_tournoi(db, tournoi)

@router.post("/joueur/")
def create_joueur_route(joueur: JoueurCreate, db: Session = Depends(get_db)):
    return create_joueur(db, joueur)

@router.post("/match/")
def create_match_route(match: MatchCreate, db: Session = Depends(get_db)):
    return create_match(db, match)

@router.put("/match/{match_id}/score")
def update_match_score_route(match_id: int, match_update: MatchScoreUpdate, db: Session = Depends(get_db)):
    match = update_match_score(db, match_id, match_update)
    if not match:
        raise HTTPException(status_code=404, detail="Match non trouvé")
    return match

@router.get("/tournoi/{tournoi_id}/matchs")
def get_tournoi_matchs(tournoi_id: int, db: Session = Depends(get_db)):
    matchs = db.query(Match).filter(Match.tournoi_id == tournoi_id).all()
    return matchs

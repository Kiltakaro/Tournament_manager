from sqlalchemy.orm import Session
from models import Tournoi, Joueur, Match
from schemas import TournoiCreate, JoueurCreate, MatchCreate, MatchScoreUpdate

def create_tournoi(db: Session, tournoi: TournoiCreate):
    db_tournoi = Tournoi(nom=tournoi.nom)
    db.add(db_tournoi)
    db.commit()
    db.refresh(db_tournoi)
    return db_tournoi

def create_joueur(db: Session, joueur: JoueurCreate):
    db_joueur = Joueur(nom=joueur.nom, tournoi_id=joueur.tournoi_id)
    db.add(db_joueur)
    db.commit()
    db.refresh(db_joueur)
    return db_joueur

def create_match(db: Session, match: MatchCreate):
    db_match = Match(
        tournoi_id=match.tournoi_id,
        joueur1_id=match.joueur1_id,
        joueur2_id=match.joueur2_id,
        phase=match.phase
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def update_match_score(db: Session, match_id: int, match_update: MatchScoreUpdate):
    match = db.query(Match).filter(Match.id == match_id).first()
    if match:
        match.score_joueur1 = match_update.score_joueur1
        match.score_joueur2 = match_update.score_joueur2
        match.gagnant_id = match.joueur1_id if match.score_joueur1 > match.score_joueur2 else match.joueur2_id
        db.commit()
        db.refresh(match)
        return match
    return None

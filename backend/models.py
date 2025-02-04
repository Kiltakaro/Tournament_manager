from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Tournoi(Base):
    __tablename__ = "tournois"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    date_creation = Column(TIMESTAMP, default=datetime.utcnow)

class Joueur(Base):
    __tablename__ = "joueurs"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    tournoi_id = Column(Integer, ForeignKey("tournois.id", ondelete="CASCADE"))

class Match(Base):
    __tablename__ = "matchs"
    id = Column(Integer, primary_key=True, index=True)
    tournoi_id = Column(Integer, ForeignKey("tournois.id", ondelete="CASCADE"))
    joueur1_id = Column(Integer, ForeignKey("joueurs.id", ondelete="SET NULL"))
    joueur2_id = Column(Integer, ForeignKey("joueurs.id", ondelete="SET NULL"))
    score_joueur1 = Column(Integer, default=0)
    score_joueur2 = Column(Integer, default=0)
    phase = Column(String, nullable=False)  # 'poule' ou 'elimination'
    gagnant_id = Column(Integer, ForeignKey("joueurs.id", ondelete="SET NULL"))

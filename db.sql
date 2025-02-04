CREATE TABLE tournois (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    date_creation TIMESTAMP DEFAULT NOW()
);

CREATE TABLE joueurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    tournoi_id INT REFERENCES tournois(id) ON DELETE CASCADE
);

CREATE TABLE matchs (
    id SERIAL PRIMARY KEY,
    tournoi_id INT REFERENCES tournois(id) ON DELETE CASCADE,
    joueur1_id INT REFERENCES joueurs(id) ON DELETE SET NULL,
    joueur2_id INT REFERENCES joueurs(id) ON DELETE SET NULL,
    score_joueur1 INT DEFAULT 0,
    score_joueur2 INT DEFAULT 0,
    phase VARCHAR(50) CHECK (phase IN ('poule', 'elimination')),
    gagnant_id INT REFERENCES joueurs(id) ON DELETE SET NULL
);

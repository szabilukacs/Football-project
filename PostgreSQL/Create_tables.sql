
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS teams;
-- DROP TABLE IF EXISTS divisions;

-- ezt kesobb majd csak
/*
-- 0. Diviziok táblája
CREATE TABLE divisions (
    division_id VARCHAR(5) PRIMARY KEY,
    division_name VARCHAR(50) NOT NULL UNIQUE -- ide majd megadni hosszan is masik rtekben a nevet
);
*/

-- 1. Csapatok táblája
CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Meccsek táblája
CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    match_date DATE NOT NULL,
    home_team_id INT NOT NULL REFERENCES teams(team_id),
    away_team_id INT NOT NULL REFERENCES teams(team_id),
	division_name CHAR(4),
    ft_home_goals INT,
    ft_away_goals INT,
    ft_result CHAR(1),  -- H / D / A
	home_elo INT,
    away_elo INT,
    home_form3 INT,
    home_form5 INT,
    away_form3 INT,
    away_form5 INT,	
    ht_home_goals INT,
    ht_away_goals INT,
    ht_result CHAR(1),   -- H / D / A
	home_shots INT,
    away_shots INT,
    home_target INT,
    away_target INT,
    home_fouls INT,
    away_fouls INT,
    home_corners INT,
    away_corners INT,
    home_yellow INT,
    away_yellow INT,
    home_red INT,
    away_red INT
);

-- Indexek a gyors kereséshez
CREATE INDEX idx_matches_date ON matches(match_date);
CREATE INDEX idx_matches_teams ON matches(home_team_id, away_team_id);

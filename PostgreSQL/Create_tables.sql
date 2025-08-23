
DROP TABLE IF EXISTS elo_history;
DROP TABLE IF EXISTS match_stats;
DROP TABLE IF EXISTS team_form;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS divisions;

-- 0. Diviziok táblája
CREATE TABLE divisions (
    division_id SERIAL PRIMARY KEY,
    division_name VARCHAR(20) NOT NULL UNIQUE
);

-- 1. Csapatok táblája
CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(50) NOT NULL UNIQUE,
	division_id INT NOT NULL REFERENCES divisions(division_id) ON DELETE CASCADE
);

-- 2. Meccsek táblája
CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    match_date DATE NOT NULL,
    home_team_id INT NOT NULL REFERENCES teams(team_id),
    away_team_id INT NOT NULL REFERENCES teams(team_id),
    ft_home_goals INT,
    ft_away_goals INT,
    ft_result CHAR(1),  -- H / D / A
    ht_home_goals INT,
    ht_away_goals INT,
    ht_result CHAR(1)   -- H / D / A
);

-- 3. Meccs statisztikák
CREATE TABLE match_stats (
    stat_id SERIAL PRIMARY KEY,
    match_id INT NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
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

-- 4. Formák (utolsó 3 és 5 meccs a mérkőzés pillanatában)
CREATE TABLE team_form (
    form_id SERIAL PRIMARY KEY,
    team_id INT NOT NULL REFERENCES teams(team_id),
    match_id INT NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
    form3 INT,
    form5 INT
);

-- 5. Elo történet (mérkőzés előtti és utáni értékek)
CREATE TABLE elo_history (
    elo_id SERIAL PRIMARY KEY,
    team_id INT NOT NULL REFERENCES teams(team_id),
    match_id INT NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
    elo_before NUMERIC(8,2),
    elo_after NUMERIC(8,2)
);

-- Indexek a gyors kereséshez
CREATE INDEX idx_matches_date ON matches(match_date);
CREATE INDEX idx_matches_teams ON matches(home_team_id, away_team_id);
CREATE INDEX idx_elo_team ON elo_history(team_id);

CREATE OR REPLACE VIEW avg_goals_per_team AS
SELECT 
    t.team_name,
    AVG(m.ft_home_goals) AS avg_home_goals,
    AVG(m.ft_away_goals) AS avg_away_goals,
    (AVG(m.ft_home_goals) + AVG(m.ft_away_goals)) / 2 AS avg_total_goals
FROM matches m
JOIN teams t ON t.team_id = m.home_team_id
GROUP BY t.team_name;

CREATE OR REPLACE VIEW win_ratio_per_team AS
SELECT
    t.team_name,
    SUM(CASE WHEN m.ft_result = 'H' AND t.team_id = m.home_team_id THEN 1
             WHEN m.ft_result = 'A' AND t.team_id = m.away_team_id THEN 1 ELSE 0 END) 
             / NULLIF(COUNT(*),0)::float AS win_ratio
FROM matches m
JOIN teams t ON t.team_id = m.home_team_id OR t.team_id = m.away_team_id
GROUP BY t.team_name;

CREATE OR REPLACE VIEW division_stats AS
SELECT
    division_name,
    COUNT(*) AS total_matches,
    AVG(ft_home_goals + ft_away_goals) AS avg_goals_per_match
FROM matches
GROUP BY division_name;

-- 1. ELO trend: átlag ELO időben (csapatonként, top 20)
-- 1. ELO trend: átlag ELO időben (csapatonként, top 20)
-- drop view v_team_elo_trend;
CREATE OR REPLACE VIEW v_team_elo_trend AS
SELECT 
    t.team_name,
    DATE_TRUNC('month', m.match_date) AS month,
    COALESCE(
        ROUND(
            AVG(
                CASE 
                    WHEN m.home_team_id = t.team_id THEN COALESCE(m.home_elo,0)
                    ELSE COALESCE(m.away_elo,0)
                END
            ),
        2),
    0) AS avg_elo
FROM matches m
JOIN teams t ON t.team_id IN (m.home_team_id, m.away_team_id)
GROUP BY t.team_name, DATE_TRUNC('month', m.match_date)
ORDER BY avg_elo DESC
LIMIT 20;


CREATE OR REPLACE VIEW v_team_shooting_efficiency AS
SELECT 
    t.team_name,
    COUNT(*) AS matches_played,
    COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_shots ELSE m.away_shots END), 0) AS total_shots,
    COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_target ELSE m.away_target END), 0) AS total_on_target,
    COALESCE(
        ROUND(
            COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_target ELSE m.away_target END), 0)::numeric /
            NULLIF(COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_shots ELSE m.away_shots END), 0), 0), 
            3
        ),
        0
    ) AS shooting_accuracy
FROM matches m
JOIN teams t ON t.team_id IN (m.home_team_id, m.away_team_id)
GROUP BY t.team_name
ORDER BY shooting_accuracy DESC
LIMIT 20;


-- 3. Fouls / lapok: agresszivitás mutató
CREATE OR REPLACE VIEW v_team_aggressiveness AS
SELECT 
    t.team_name,
    COUNT(*) AS matches_played,
    COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_fouls ELSE m.away_fouls END), 0) AS total_fouls,
    COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_yellow ELSE m.away_yellow END), 0) AS total_yellow,
    COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_red ELSE m.away_red END), 0) AS total_red,
    COALESCE(
        ROUND(
            (
                COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_yellow ELSE m.away_yellow END),0)*0.5 +
                COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_red ELSE m.away_red END),0)*1 +
                COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_fouls ELSE m.away_fouls END),0)*0.1
            ) / COUNT(*),
            2
        ),
        0
    ) AS aggressiveness_score
FROM matches m
JOIN teams t ON t.team_id IN (m.home_team_id, m.away_team_id)
GROUP BY t.team_name
ORDER BY aggressiveness_score DESC
LIMIT 20;

-- 4. Csapat hatékonysági mutató: gól/lövés, gól/kapura lövés
CREATE OR REPLACE VIEW v_team_scoring_efficiency AS
SELECT 
    t.team_name,
    COUNT(*) AS matches_played,
    COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.ft_home_goals ELSE m.ft_away_goals END), 0) AS total_goals,
    COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_shots ELSE m.away_shots END), 0) AS total_shots,
    COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_target ELSE m.away_target END), 0) AS total_on_target,
    COALESCE(
        ROUND(
            COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.ft_home_goals ELSE m.ft_away_goals END),0)::numeric /
            NULLIF(COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_shots ELSE m.away_shots END),0),0),
            3
        ),
        0
    ) AS goals_per_shot,
    COALESCE(
        ROUND(
            COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.ft_home_goals ELSE m.ft_away_goals END),0)::numeric /
            NULLIF(COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_target ELSE m.away_target END),0),0),
            3
        ),
        0
    ) AS goals_per_on_target
FROM matches m
JOIN teams t ON t.team_id IN (m.home_team_id, m.away_team_id)
GROUP BY t.team_name
ORDER BY goals_per_shot DESC
LIMIT 20;

-- 5. Gólkülönbségek (heatmaphez)
CREATE OR REPLACE VIEW v_team_goal_difference AS
SELECT 
    ht.team_name AS home_team,
    at.team_name AS away_team,
    COALESCE(SUM(m.ft_home_goals - m.ft_away_goals), 0) AS goal_difference
FROM matches m
JOIN teams ht ON ht.team_id = m.home_team_id
JOIN teams at ON at.team_id = m.away_team_id
GROUP BY ht.team_name, at.team_name
ORDER BY ABS(SUM(m.ft_home_goals - m.ft_away_goals)) DESC
LIMIT 20;

-- select * from v_team_elo_trend;





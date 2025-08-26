select * from teams;
select * from matches where division_name = 'ROM';
select * from matches WHERE ft_home_goals is null;

select * from teams where team_name = "ferencvaros";

CREATE OR REPLACE VIEW win_ratio_per_team AS
SELECT
    t.team_name,
    SUM(CASE WHEN m.ft_result = 'H' AND t.team_id = m.home_team_id THEN 1
             WHEN m.ft_result = 'A' AND t.team_id = m.away_team_id THEN 1 ELSE 0 END) 
             / NULLIF(COUNT(*),0)::float AS win_ratio
FROM matches m
JOIN teams t ON t.team_id = m.home_team_id OR t.team_id = m.away_team_id
GROUP BY t.team_name;



select * from win_ratio_per_team;

drop view avg_goals_per_team;




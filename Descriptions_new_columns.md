This file include descriptions for new columns.


Functions:
1) Ft_eng_match_date()
home_team_days_betw_games = [f'home_team_days_betw_games_{i}' for i in range(1,11)] - number of days between games of the home team
away_team_days_betw_games = [f'away_team_days_betw_games_{i}' for i in range(1,11)] - number of days between games of the away team

"home_team_avg_days_betw_games" - average number of days between home team games
"away_team_avg_days_betw_games" - average number of days between away team games

home_diff_date = [f'home_diff_date_{i}' for i in range(1,11)] - the number of days between match_date and the rest of the home team matches
away_diff_date = [f'away_diff_date_{i}' for i in range(1,11)] - the number of days between match_date and the rest of the away team matches

"home_team_last_game_this_week" - the last home team game was no more than a week ago
"away_team_last_game_this_week" - the last away team game was no more than a week ago

"month" - game month
"weekday" - game day
"hour" - hour game
"is_weekend" - weekend yes/no
"is_football_season" - the game was during the soccer season - from September to May

2) Ft_eng_is_play_home()
"home_count_home_games" - the number of home games of the home team
"away_count_home_games" - the number of home games of the away team

3) Ft_eng_is_cup()
"home_count_cup_games" - number of cup meetings of the home team
"away_count_cup_games" - number of cup meetings of the away team

4) Ft_eng_history_goal()
"home_goals_scored" - the number of goals scored by the home team
"home_goals_conceded" - the number of goals conceded by the home team
"away_goals_scored" - the number of goals scored by the away team
"away_goals_conceded" - the number of goals conceded by the away team

home_team_win = [f'home_team_win_{i}' for i in range(1,11)] - home team result tags. # 1 - win, 0 - loss, 2 - draw.
away_team_win = [f'away_team_win_{i}' for i in range(1,11)] - away team result tags. # 1 - win, 0 - loss, 2 - draw.

"home_team_points" - the number of points earned by the home team over the last 10 games
"away_team_points" - the number of points earned by the away team over the last 10 games

"home_team_count_win" - the number of wins of the home team over the last 10 games
"away_team_count_win" - the number of wins of the away team over the last 10 games
"home_team_count_lose" - the number of loses of the home team over the last 10 games
"away_team_count_lose" - the number of loses of the away team over the last 10 games
"home_team_count_draw" - the number of draws of the home team over the last 10 games
"away_team_count_draw" - the number of draws of the away team over the last 10 games

"home_team_streak_wins" - streak of wins of the home team
"away_team_streak_wins" - streak of wins of the away team
"home_team_streak_loses" - streak of losses of the home team
"away_team_streak_loses"- streak of losses of the home team

5) Ft_eng_win_percentage()
"home_team_perc_win_home" - home team winning percentage
"home_team_perc_win_away" - the percentage of away wins for the home team
"away_team_perc_win_home" - away team winning percentage
"away_team_perc_win_away" - the percentage of away wins for the away team
"home_team_perc_win_cup" - the percentage of wins in cup matches of the home team
"away_team_perc_win_cup" - the percentage of wins in cup matches of the away team

6) Ft_eng_rating()
"home_team_mean_rating" - home team rating
"away_team_mean_rating" - away team rating

"mean_rating_in_league" - league average rating

"home_team_diff_rating_league" - the difference between the average league rating and the home team rating
"away_team_diff_rating_league" - the difference between the average league rating and the away team rating
"home_team_mean_rating_general" - overall average home team rating
"away_team_mean_rating_general" - overall average away team rating

home_team_history_ELO_rating = [f'home_team_history_ELO_rating_{i}' for i in range(1,11)] - ELO-rating of home team
away_team_history_ELO_rating = [f'away_team_history_ELO_rating_{i}' for i in range(1,11)] - ELO-rating of away team
"home_team_ELO_rating" - mean ELO-rating of home team for the last 10 days
"away_team_ELO_rating" - mean ELO-rating of away team for the last 10 days

"home_team_rank" - rank of the home team
"away_team_rank" - rank of the away team

7) Ft_eng_league_id()
"home_team_count_league" - the number of leagues the home team
"away_team_count_league" - the number of leagues the away team

"home_team_same_league" - the last 10 games the home team has played in the same league - True/False
"away_team_same_league" - the last 10 games the away team has played in the same league - True/False

8) Ft_eng_coach_id()
"home_team_count_coach" - the number of coaches on the home team
"away_team_count_coach" - the number of coaches on the away team

"home_team_same_coach" - the last 10 games the home team has same coach - True/False
"away_team_same_coach" - the last 10 games the away team has same coach - True/False

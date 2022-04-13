import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from tqdm.notebook import trange, tqdm

class FeaturesEngineering:
    def __init__(self, dataset):
        self.dataset = dataset
       
    def Ft_eng_match_date(self):
        ''' 
        Create the following columns:
            home_team_days_betw_games_1-10; away_team_days_betw_games_1-10; "home_team_avg_days_betw_games", "away_team_avg_days_betw_games"; home_diff_date_1-10; away_diff_date_1-10; "home_team_last_game_this_week", "away_team_last_game_this_week";
            "month"; "weekday"; "hour"; "is_weekend"; "is_football_season"
        For more detail see the file "Descriptions_new_columns"
        '''
        match_dates_home = ['match_date'] + [f'home_team_history_match_date_{i}' for i in range(1,11)]
        match_dates_away = ['match_date'] + [f'away_team_history_match_date_{i}' for i in range(1,11)]
        home_team_days_betw_games = [f'home_team_days_betw_games_{i}' for i in range(1,11)]
        away_team_days_betw_games = [f'away_team_days_betw_games_{i}' for i in range(1,11)]
        home_diff_date = [f'home_diff_date_{i}' for i in range(1,11)]
        away_diff_date = [f'away_diff_date_{i}' for i in range(1,11)]
        
        # home_team_days_betw_games
        for i in range(10):
            self.dataset[f'home_team_days_betw_games_{i+1}'] = (self.dataset[match_dates_home[i]] -       self.dataset[match_dates_home[i+1]]).dt.days
            self.dataset[f'away_team_days_betw_games_{i+1}'] = (self.dataset[match_dates_away[i]] - self.dataset[match_dates_away[i+1]]).dt.days
        
        # outliers processing and log
        for i in home_team_days_betw_games+away_team_days_betw_games:
                self.dataset[i] = self.dataset[i].apply(lambda x: np.random.randint(30,50) if x > 50 else x)
           
        # avg_days_betw_games        
        self.dataset['home_team_avg_days_betw_games'] = self.dataset[home_team_days_betw_games].mean(axis=1)
        self.dataset['away_team_avg_days_betw_games'] = self.dataset[away_team_days_betw_games].mean(axis=1)
        
        # diff_days_matchdate_to_all_previous_games
        for i in range(1,11):
            self.dataset[f'home_diff_date_{i}'] = (self.dataset['match_date']- self.dataset[f'home_team_history_match_date_{i}']).dt.days
            self.dataset[f'away_diff_date_{i}'] = (self.dataset['match_date']- self.dataset[f'away_team_history_match_date_{i}']).dt.days
        
        # last game was during last week - [True, False]
        self.dataset['home_team_last_game_this_week'] = self.dataset['home_team_days_betw_games_1'].apply(lambda x: 1 if x<=7 else 0)
        self.dataset['away_team_last_game_this_week'] = self.dataset['away_team_days_betw_games_1'].apply(lambda x: 1 if x<=7 else 0)
        
        # month, weekday, hour, is_weekend, is_football_season
        self.dataset['month'] = self.dataset['match_date'].dt.month
        self.dataset['weekday'] = self.dataset['match_date'].dt.weekday
        self.dataset['hour'] = self.dataset['match_date'].dt.hour
        self.dataset['is_weekend'] = self.dataset['weekday'].apply(lambda x: 1 if x>=5 else 0)
        self.dataset['is_football_season'] = (~self.dataset['month'].isin([5,6,7,8])).map({True:1, False:0})
        
    def Ft_eng_is_play_home(self):
        '''
        Create the following columns:
            "home_count_home_games"; "away_count_home_games"
        For more detail see the file "Descriptions_new_columns"
        '''
        home_team_is_play_home = [f'home_team_history_is_play_home_{i}' for i in range(1,11)]
        away_team_is_play_home = [f'away_team_history_is_play_home_{i}' for i in range(1,11)]

        # count_home_games
        self.dataset['home_count_home_games'] = self.dataset[home_team_is_play_home].sum(axis=1)
        self.dataset['away_count_home_games'] = self.dataset[away_team_is_play_home].sum(axis=1)
        
    def Ft_eng_is_cup(self):
        '''
        Create the following columns:
            "home_count_cup_games"; "away_count_cup_games"
        For more detail see the file "Descriptions_new_columns"
        '''
        
        home_team_history_is_cup = [f'home_team_history_is_cup_{i}' for i in range(1,11)]
        away_team_history_is_cup = [f'away_team_history_is_cup_{i}' for i in range(1,11)]

        # count_cup_games
        self.dataset['home_count_cup_games'] = self.dataset[home_team_history_is_cup].sum(axis=1)
        self.dataset['away_count_cup_games'] = self.dataset[away_team_history_is_cup].sum(axis=1)
        
    def Ft_eng_history_goal(self):
        '''
        Create the following columns:
            "home_goals_scored"; "home_goals_conceded"; "away_goals_scored"; "away_goals_conceded"; home_team_win_1-10; away_team_win_1-10; "home_team_points"; "away_team_points"; "home_team_count_win"; "away_team_count_win";
            "home_team_count_lose"; "away_team_count_lose"; "home_team_count_draw"; "away_team_count_draw"; home_team_streak_wins; away_team_streak_wins; "home_team_streak_loses"; "away_team_streak_loses"
        For more detail see the file "Descriptions_new_columns"
        '''
        
        # the number of goals scored by the team
        self.dataset['home_goals_scored'] = self.dataset[[f'home_team_history_goal_{i}' for i in range(1,11)]].sum(axis=1)
        self.dataset['home_goals_conceded'] = self.dataset[[f'home_team_history_opponent_goal_{i}' for i in range(1,11)]].sum(axis=1)
        self.dataset['away_goals_scored'] = self.dataset[[f'away_team_history_goal_{i}' for i in range(1,11)]].sum(axis=1)
        self.dataset['away_goals_conceded'] = self.dataset[[f'away_team_history_opponent_goal_{i}' for i in range(1,11)]].sum(axis=1)
        # 1 - win, 0 - loss, 2 - draw.

        def function(x):
            if x>0:
                return 1
            elif x<0:
                return 0
            else:
                return 2
        for i in range(1,11):    
            self.dataset[f'home_team_win_{i}'] = (self.dataset[f'home_team_history_goal_{i}'] - self.dataset[f'home_team_history_opponent_goal_{i}']).apply(lambda x: function(x))
            self.dataset[f'away_team_win_{i}'] = (self.dataset[f'away_team_history_goal_{i}'] - self.dataset[f'away_team_history_opponent_goal_{i}']).apply(lambda x: function(x))
          
        
        # team point for last 10 games
        self.dataset['home_team_points'] = self.dataset[[f'home_team_win_{i}' for i in range(1,11)]].apply(lambda x: x.map({1:3,2:1,0:0})).sum(axis=1)
        self.dataset['away_team_points'] = self.dataset[[f'away_team_win_{i}' for i in range(1,11)]].apply(lambda x: x.map({1:3,2:1,0:0})).sum(axis=1)
        
        # count of wins, loses and draws for the last 10 days
        self.dataset['home_team_count_win'] = self.dataset[[f'home_team_win_{i}' for i in range(1,11)]].apply(lambda x: len(x[x==1]), axis=1)
        self.dataset['away_team_count_win'] = self.dataset[[f'away_team_win_{i}' for i in range(1,11)]].apply(lambda x: len(x[x==1]), axis=1)
        
        self.dataset['home_team_count_lose'] = self.dataset[[f'home_team_win_{i}' for i in range(1,11)]].apply(lambda x: len(x[x==0]), axis=1)
        self.dataset['away_team_count_lose'] = self.dataset[[f'away_team_win_{i}' for i in range(1,11)]].apply(lambda x: len(x[x==0]), axis=1)       
        
        self.dataset['home_team_count_draw'] = self.dataset[[f'home_team_win_{i}' for i in range(1,11)]].apply(lambda x: len(x[x==2]), axis=1)
        self.dataset['away_team_count_draw'] = self.dataset[[f'away_team_win_{i}' for i in range(1,11)]].apply(lambda x: len(x[x==2]), axis=1)
        
        #streak
        def funct(x):
            sum = 0
            for i in x:
                if i !=0:
                    sum+=1
                else:
                    return sum
            return sum
        
        self.dataset['home_team_streak_wins'] = self.dataset[[f'home_team_win_{i}' for i in range(1,11)]].apply(lambda x: funct(x), axis=1)
        self.dataset['away_team_streak_wins'] = self.dataset[[f'away_team_win_{i}' for i in range(1,11)]].apply(lambda x: funct(x), axis=1)
        
        def funct_lose(x):
            sum = 0
            for i in x:
                if i == 0:
                    sum+=1
                else:
                    return sum
            return sum
        self.dataset['home_team_streak_loses'] = self.dataset[[f'home_team_win_{i}' for i in range(1,11)]].apply(lambda x: funct_lose(x), axis=1)
        self.dataset['away_team_streak_loses'] = self.dataset[[f'away_team_win_{i}' for i in range(1,11)]].apply(lambda x: funct_lose(x), axis=1)
        
    def Ft_eng_win_percentage(self):
        '''
        Create the following columns:
            "home_team_perc_win_home"; "home_team_perc_win_away"; "away_team_perc_win_home"; "away_team_perc_win_away"; "home_team_perc_win_cup"; "away_team_perc_win_cup"
        For more detail see the file "Descriptions_new_columns"
        '''
        
        # The winning percentage of home games of the team
        self.dataset['home_team_perc_win_home'] = np.NaN
        for indx in tqdm(self.dataset.index):
            summ = 0
            for i in range(1,11):
                if self.dataset.loc[indx,f'home_team_win_{i}'] == 1 and self.dataset.loc[indx,f'home_team_history_is_play_home_{i}'] == 1:
                    summ +=1
            self.dataset.loc[indx,'home_team_perc_win_home'] = summ/self.dataset.loc[indx,'home_count_home_games']
        
        self.dataset['away_team_perc_win_home'] = np.NaN
        for indx in tqdm(self.dataset.index):
            summ = 0
            for i in range(1,11):
                if self.dataset.loc[indx,f'away_team_win_{i}'] == 1 and self.dataset.loc[indx,f'away_team_history_is_play_home_{i}'] == 1:
                    summ +=1
            self.dataset.loc[indx,'away_team_perc_win_home'] = summ/self.dataset.loc[indx,'away_count_home_games']
            
        # The winning percentage of away games of the team 
        self.dataset['home_team_perc_win_away'] = np.NaN
        for indx in tqdm(self.dataset.index):
            summ = 0
            for i in range(1,11):
                if self.dataset.loc[indx,f'home_team_win_{i}'] == 1 and self.dataset.loc[indx,f'home_team_history_is_play_home_{i}'] == 0:
                    summ +=1
            self.dataset.loc[indx,'home_team_perc_win_away'] = summ/(10-self.dataset.loc[indx,'home_count_home_games'])
        
        self.dataset['away_team_perc_win_away'] = np.NaN
        for indx in tqdm(self.dataset.index):
            summ = 0
            for i in range(1,11):
                if self.dataset.loc[indx,f'away_team_win_{i}'] == 1 and self.dataset.loc[indx,f'away_team_history_is_play_home_{i}'] == 0:
                    summ +=1
            self.dataset.loc[indx,'away_team_perc_win_away'] = summ/(10-self.dataset.loc[indx,'away_count_home_games'])
        
        # percentage of wins at Cup
        self.dataset['home_team_perc_win_cup'] = np.NaN
        for indx in tqdm(self.dataset.index):
            summ = 0
            for i in range(1,11):
                if self.dataset.loc[indx,f'home_team_win_{i}'] == 1 and self.dataset.loc[indx,f'home_team_history_is_cup_{i}'] == 1:
                    summ +=1
            self.dataset.loc[indx,'home_team_perc_win_cup'] = summ/self.dataset.loc[indx,'home_count_cup_games']
        
        self.dataset['away_team_perc_win_cup'] = np.NaN
        for indx in tqdm(self.dataset.index):
            summ = 0
            for i in range(1,11):
                if self.dataset.loc[indx,f'away_team_win_{i}'] == 1 and self.dataset.loc[indx,f'away_team_history_is_cup_{i}'] == 1:
                    summ +=1
            self.dataset.loc[indx,'away_team_perc_win_cup'] = summ/self.dataset.loc[indx,'away_count_cup_games']
        self.dataset.fillna(0, inplace=True)
    
    def Ft_eng_rating(self):
        '''
        Create the following columns:
            "home_team_mean_rating"; "away_team_mean_rating"; "mean_rating_in_league"; "home_team_diff_rating_league"; "away_team_diff_rating_league"; "home_team_mean_rating_general";
            "away_team_mean_rating_general"; home_team_history_ELO_rating_1-10; away_team_history_ELO_rating_1-10; "home_team_ELO_rating"; "away_team_ELO_rating"; "home_team_rank"; "away_team_rank"
        For more detail see the file "Descriptions_new_columns"
        '''
        home_team_history_rating = [f'home_team_history_rating_{i}' for i in range(1,11)]
        away_team_history_rating = [f'away_team_history_rating_{i}' for i in range(1,11)]
        self.dataset['home_team_mean_rating'] = self.dataset[home_team_history_rating].mean(axis=1)
        self.dataset['away_team_mean_rating'] = self.dataset[away_team_history_rating].mean(axis=1)
        
        # mean rating team in each league_name
        home_league = self.dataset[['league_name', 'home_team_mean_rating']].reset_index().drop(['id'],axis=1).rename(columns={'league_name':'league_name',"home_team_mean_rating":"rating"})
        away_league = self.dataset[['league_name', 'away_team_mean_rating']].reset_index().drop(['id'],axis=1).rename(columns={'league_name':'league_name',"away_team_mean_rating":"rating"})
        all_team_league = pd.concat([home_league,away_league])
        self.dataset['mean_rating_in_league'] = self.dataset['league_name'].map(all_team_league.groupby(['league_name'])['rating'].mean().to_dict())
        
        # diff = team_rating - mean_rating_league
        self.dataset['home_team_diff_rating_league'] = self.dataset['home_team_mean_rating'] - self.dataset['mean_rating_in_league']
        self.dataset['away_team_diff_rating_league'] = self.dataset['away_team_mean_rating'] - self.dataset['mean_rating_in_league']
        
        # mean rating each team
        home_team = self.dataset[['home_team_name', 'home_team_mean_rating']].reset_index().drop(['id'],axis=1).rename(columns={'home_team_name':'team_name',"home_team_mean_rating":"rating"})
        away_team = self.dataset[['away_team_name', 'away_team_mean_rating']].reset_index().drop(['id'],axis=1).rename(columns={'away_team_name':'team_name',"away_team_mean_rating":"rating"})
        all_team_team = pd.concat([home_team,away_team])
        self.dataset['home_team_mean_rating_general'] = self.dataset['home_team_name'].map(all_team_team.groupby('team_name')['rating'].mean().to_dict())
        self.dataset['away_team_mean_rating_general'] = self.dataset['away_team_name'].map(all_team_team.groupby('team_name')['rating'].mean().to_dict())
        
        #rank
        rank = all_team_team.groupby('team_name')['rating'].mean().sort_values(ascending=False).index
        self.dataset['home_team_rank'] = self.dataset['home_team_name'].map({rank[i]:i+1 for i in range(len(rank))})
        self.dataset['away_team_rank'] = self.dataset['away_team_name'].map({rank[i]:i+1 for i in range(len(rank))})
        
        # ELO_rating
        for i in range(1,11):
            self.dataset[f'home_team_history_ELO_rating_{i}'] = 1/(1+10**((self.dataset[f'home_team_history_opponent_rating_{i}']-self.dataset[f'home_team_history_rating_{i}'])/10))
            self.dataset[f'away_team_history_ELO_rating_{i}'] = 1/(1+10**((self.dataset[f'away_team_history_opponent_rating_{i}']-self.dataset[f'away_team_history_rating_{i}'])/10))
        
        self.dataset['home_team_ELO_rating'] = self.dataset[[f'home_team_history_ELO_rating_{i}' for i in range(1,11)]].mean(axis=1)
        self.dataset['away_team_ELO_rating'] = self.dataset[[f'away_team_history_ELO_rating_{i}' for i in range(1,11)]].mean(axis=1)
        
    def Ft_eng_league_id(self):
        '''
        Create the following columns:
            "home_team_count_league"; "away_team_count_league"; "home_team_same_league"; "away_team_same_league"
        For more detail see the file "Descriptions_new_columns"
        '''
        away_team_history_league = [f'away_team_history_league_id_{i}' for i in range(1,11)]
        home_team_history_league = [f'home_team_history_league_id_{i}' for i in range(1,11)]
        self.dataset['home_team_count_league'] = self.dataset[['league_id'] + home_team_history_league].apply(lambda x: len(set(x)),axis=1)
        self.dataset['away_team_count_league'] = self.dataset[['league_id'] + away_team_history_league].apply(lambda x: len(set(x)),axis=1)

        self.dataset['home_team_same_league'] = self.dataset['home_team_count_league'].apply(lambda x: x==1).map({True:1,False:0})
        self.dataset['away_team_same_league'] = self.dataset['away_team_count_league'].apply(lambda x: x==1).map({True:1,False:0})
        
    def Ft_eng_coach_id(self):
        '''
        Create the following columns:
            "home_team_count_coach"; "away_team_count_coach"; "home_team_same_coach"; "away_team_same_coach"
        For more detail see the file "Descriptions_new_columns"
        '''
        home_team_history_coach = [f'home_team_history_coach_{i}' for i in range(1,11)]
        away_team_history_coach = [f'away_team_history_coach_{i}' for i in range(1,11)]
        

        self.dataset['home_team_count_coach'] = self.dataset[['home_team_coach_id'] + home_team_history_coach].apply(lambda x: len(set(x)),axis=1)
        self.dataset['away_team_count_coach'] = self.dataset[['away_team_coach_id'] + home_team_history_coach].apply(lambda x: len(set(x)),axis=1)
        
        self.dataset['home_team_same_coach'] = self.dataset['home_team_count_coach'].apply(lambda x: x==1).map({True:1,False:0})
        self.dataset['away_team_same_coach'] = self.dataset['home_team_count_coach'].apply(lambda x: x==1).map({True:1,False:0})
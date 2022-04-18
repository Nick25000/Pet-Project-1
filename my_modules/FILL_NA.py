from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler


class FillNa:
    def __init__(self, dataset):
        self.dataset = dataset
        # descriptive_columns
        self.descriptive_columns = ['home_team_name', 'away_team_name', 'match_date', 'league_name',
                                    'league_id', 'is_cup']
        # coachs_id_columns
        self.coachs_columns = ['home_team_coach_id', 'away_team_coach_id'] \
                              + [f'home_team_history_coach_{i}' for i in range(1, 11)] \
                              + [f'away_team_history_coach_{i}' for i in range(1, 11)]

        # times_columns
        self.home_team_history_match_dates = ['match_date'] + [f'home_team_history_match_date_{i}' for i in
                                                               range(1, 11)]
        self.away_team_history_match_dates = ['match_date'] + [f'away_team_history_match_date_{i}' for i in
                                                               range(1, 11)]

        # team_is_play_home_columns
        self.home_team_is_play_home = [f'home_team_history_is_play_home_{i}' for i in range(1, 11)]
        self.away_team_is_play_home = [f'away_team_history_is_play_home_{i}' for i in range(1, 11)]
        self.all_team_is_play_home = self.home_team_is_play_home + self.away_team_is_play_home

        # team_history_is_cup_columns
        self.home_team_history_is_cup = [f'home_team_history_is_cup_{i}' for i in range(1, 11)]
        self.away_team_history_is_cup = [f'away_team_history_is_cup_{i}' for i in range(1, 11)]

        # team_history_goal_columns
        self.home_team_history_goal = [f'home_team_history_goal_{i}' for i in range(1, 11)]
        self.away_team_history_goal = [f'away_team_history_goal_{i}' for i in range(1, 11)]
        self.home_team_history_opponent_goal = [f'home_team_history_opponent_goal_{i}' for i in range(1, 11)]
        self.away_team_history_opponent_goal = [f'away_team_history_opponent_goal_{i}' for i in range(1, 11)]

        # team_history_rating_columns
        self.home_team_history_rating = [f'home_team_history_rating_{i}' for i in range(1, 11)]
        self.away_team_history_rating = [f'away_team_history_rating_{i}' for i in range(1, 11)]
        self.home_team_history_opponent_rating = [f'home_team_history_opponent_rating_{i}' for i in range(1, 11)]
        self.away_team_history_opponent_rating = [f'away_team_history_opponent_rating_{i}' for i in range(1, 11)]

        # team_history_league_id_columns
        self.away_team_history_league = [f'away_team_history_league_id_{i}' for i in range(1, 11)]
        self.home_team_history_league = [f'home_team_history_league_id_{i}' for i in range(1, 11)]

    def fill_na_descr_col(self):
        """There is one position with NA values in columns "home_team_name" and "away_team_name".
        So we can delete the whole position from dataset"""
        drop_index = self.dataset[self.dataset['home_team_name'].isna()].index
        self.dataset.drop(drop_index, axis=0, inplace=True)
        assert self.dataset[self.descriptive_columns].isna().sum().sum() == 0

    def fill_na_coachs(self, astype_int=True, lb_encoder=False):
        """ Fill NA-values with the values of the previous 'coach_history_id'. And finnaly with zeros
        astype_int:[True, False] - convert to type 'int64'
        lb_encoder:[True, False] - apply LabelEncoder()
        """
        home_coachs_columns = ['home_team_coach_id'] + [f'home_team_history_coach_{i}' for i in range(1, 11)]
        away_coachs_columns = ['away_team_coach_id'] + [f'away_team_history_coach_{i}' for i in range(1, 11)]

        # fill NA-values in main columns - "home_team_coach_id", "away_team_coach_id" with other columns
        for i in home_coachs_columns[1:]:
            self.dataset['home_team_coach_id'].fillna(self.dataset[i], inplace=True)
        self.dataset['home_team_coach_id'].fillna(0, inplace=True)
        for i in away_coachs_columns[1:]:
            self.dataset['away_team_coach_id'].fillna(self.dataset[i], inplace=True)
        self.dataset['away_team_coach_id'].fillna(0, inplace=True)

        # fill Na-values in history's columns
        for i in home_coachs_columns[1:]:
            self.dataset[i].fillna(self.dataset['home_team_coach_id'], inplace=True)
        for i in away_coachs_columns[1:]:
            self.dataset[i].fillna(self.dataset['away_team_coach_id'], inplace=True)
        # check
        assert self.dataset[self.coachs_columns].isna().sum().sum() == 0

        # type to int
        if astype_int:
            self.dataset[self.coachs_columns] = self.dataset[self.coachs_columns].astype('int64')
        if not lb_encoder:
            return
        # LabelEncoder
        all_coach_id = list(set(self.dataset[self.coachs_columns].stack()))
        le = LabelEncoder()
        le.fit(all_coach_id)
        for i in self.coachs_columns:
            self.dataset[i] = le.transform(self.dataset[i])

    def fill_na_time(self):
        """ Convert to pandas datetime and fill NA-values with the previous data-values + 7-days timedelta
        """
        # identify function - convert to pandas datetime
        function_to_date = lambda x: datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S")

        # fill NA-values with the previous values + 7 days
        for num, i in enumerate(self.home_team_history_match_dates[1:]):
            values_for_compl = self.dataset[self.dataset[i].isna()][self.home_team_history_match_dates[num]]
            self.dataset[i].fillna(values_for_compl.apply(function_to_date) - timedelta(days=7), inplace=True)

        for num, i in enumerate(self.away_team_history_match_dates[1:]):
            values_for_compl = self.dataset[self.dataset[i].isna()][self.away_team_history_match_dates[num]]
            self.dataset[i].fillna(values_for_compl.apply(function_to_date) - timedelta(days=7), inplace=True)

        # convert to datetime    
        for i in self.home_team_history_match_dates[1:] + self.away_team_history_match_dates[1:]:
            self.dataset[i] = self.dataset[i].apply(function_to_date)

        # check
        all_times_collumns = self.home_team_history_match_dates + self.away_team_history_match_dates[1:]
        assert self.dataset[all_times_collumns].isna().sum().sum() == 0

    def fill_na_is_play_home(self, astype_int=True):
        """
        Filling the NA-values with interleaving
        astype_int:[True, False] - convert to type 'int64'
        """

        self.dataset[self.home_team_is_play_home[0]].fillna(0.0, inplace=True)
        for num, i in enumerate(self.home_team_is_play_home[1:]):
            values_for_compl = self.dataset[self.dataset[i].isna()][self.home_team_is_play_home[num]]
            self.dataset[i].fillna(values_for_compl.apply(lambda x: 0.0 if x == 1.0 else 1.0), inplace=True)
        assert self.dataset[self.home_team_is_play_home].isna().sum().sum() == 0

        self.dataset[self.away_team_is_play_home[0]].fillna(1.0, inplace=True)
        for num, i in enumerate(self.away_team_is_play_home[1:]):
            values_for_compl = self.dataset[self.dataset[i].isna()][self.away_team_is_play_home[num]]
            self.dataset[i].fillna(values_for_compl.apply(lambda x: 0.0 if x == 1.0 else 1.0), inplace=True)
        assert self.dataset[self.away_team_is_play_home].isna().sum().sum() == 0

        if astype_int:
            self.dataset[self.all_team_is_play_home] = self.dataset[self.all_team_is_play_home].astype('int64')

    def fill_na_cup(self, astype_int=True):
        """
        Filling NA-values with random with False (dist - 92% is not cup games & 8% cup game)
        astype_int:[True, False] - convert to type 'int64'
        """
        team_history_is_cup = self.home_team_history_is_cup + self.away_team_history_is_cup
        self.dataset[team_history_is_cup] = self.dataset[team_history_is_cup].fillna(0.0)
        # from bool into (1,0)
        self.dataset['is_cup'] = self.dataset['is_cup'].map({True: 1, False: 0})

        if astype_int:
            self.dataset[team_history_is_cup] = self.dataset[team_history_is_cup].astype('int64')
        assert self.dataset[team_history_is_cup].isna().sum().sum() == 0

    def fill_na_goal_team(self):
        mean_goal = int(self.dataset[self.home_team_history_goal + self.away_team_history_goal].mean().mean())
        columns = [f'goal_{i}' for i in range(1, 11)]
        split_index = self.dataset.shape[0]

        home_goal = self.dataset[['home_team_name'] + self.home_team_history_goal].copy()
        home_goal.rename(columns={i: j for i, j in zip(self.home_team_history_goal, columns)}, inplace=True)
        home_goal.rename(columns={'home_team_name': 'team_name'}, inplace=True)
        home_goal.reset_index(drop=True, inplace=True)

        away_goal = self.dataset[['away_team_name'] + self.away_team_history_goal].copy()
        away_goal.rename(columns={i: j for i, j in zip(self.away_team_history_goal, columns)}, inplace=True)
        away_goal.rename(columns={'away_team_name': 'team_name'}, inplace=True)
        away_goal.reset_index(drop=True, inplace=True)

        all_goal = pd.concat([home_goal, away_goal], axis=0)
        all_goal['mean'] = all_goal[columns].mean(axis=1)
        maping_goal = all_goal[~all_goal['mean'].isna()].pivot_table(index='team_name', values='mean')
        maping_goal = maping_goal.astype('int')
        all_goal.set_index('team_name', inplace=True)

        list_na = {}
        for i in all_goal[all_goal['goal_1'].isna()].index:
            if i in maping_goal.index:
                list_na[i] = float(maping_goal.loc[i])
            else:
                list_na[i] = mean_goal

        all_goal['goal_1'] = all_goal['goal_1'].fillna(list_na)
        self.dataset['home_team_history_goal_1'] = list(all_goal.iloc[:split_index, :]['goal_1'])
        self.dataset['away_team_history_goal_1'] = list(all_goal.iloc[split_index:, :]['goal_1'])
        [self.dataset[i].fillna(self.dataset['home_team_history_goal_1'], inplace=True) for i in
         self.home_team_history_goal]
        [self.dataset[i].fillna(self.dataset['away_team_history_goal_1'], inplace=True) for i in
         self.away_team_history_goal]

        self.dataset[self.home_team_history_goal + self.away_team_history_goal] = self.dataset[
            self.home_team_history_goal + self.away_team_history_goal].astype('int64')
        assert self.dataset[self.home_team_history_goal + self.away_team_history_goal].isna().sum().sum() == 0

    def fill_na_goal_team_opponent(self):

        mean_goal = int(
            self.dataset[self.home_team_history_opponent_goal + self.away_team_history_opponent_goal].mean().mean())
        columns = [f'goal_{i}' for i in range(1, 11)]
        split_index = self.dataset.shape[0]

        home_goal = self.dataset[['home_team_name'] + self.home_team_history_opponent_goal].copy()
        home_goal.rename(columns={i: j for i, j in zip(self.home_team_history_opponent_goal, columns)}, inplace=True)
        home_goal.rename(columns={'home_team_name': 'team_name'}, inplace=True)
        home_goal.reset_index(drop=True, inplace=True)

        away_goal = self.dataset[['away_team_name'] + self.away_team_history_opponent_goal].copy()
        away_goal.rename(columns={i: j for i, j in zip(self.away_team_history_opponent_goal, columns)}, inplace=True)
        away_goal.rename(columns={'away_team_name': 'team_name'}, inplace=True)
        away_goal.reset_index(drop=True, inplace=True)
        all_goal = pd.concat([home_goal, away_goal], axis=0)

        all_goal['mean'] = all_goal[columns].mean(axis=1)
        maping_goal = all_goal[~all_goal['mean'].isna()].pivot_table(index='team_name', values='mean')
        maping_goal = maping_goal.astype('int')
        all_goal.set_index('team_name', inplace=True)

        list_na = {}
        for i in all_goal[all_goal['goal_1'].isna()].index:
            if i in maping_goal.index:
                list_na[i] = float(maping_goal.loc[i])
            else:
                list_na[i] = mean_goal

        all_goal['goal_1'] = all_goal['goal_1'].fillna(list_na)

        self.dataset['home_team_history_opponent_goal_1'] = list(all_goal.iloc[:split_index, :]['goal_1'])
        self.dataset['away_team_history_opponent_goal_1'] = list(all_goal.iloc[split_index:, :]['goal_1'])
        [self.dataset[i].fillna(self.dataset['home_team_history_opponent_goal_1'], inplace=True) for i in
         self.home_team_history_opponent_goal]
        [self.dataset[i].fillna(self.dataset['away_team_history_opponent_goal_1'], inplace=True) for i in
         self.away_team_history_opponent_goal]

        self.dataset[self.home_team_history_opponent_goal + self.away_team_history_opponent_goal] = self.dataset[
            self.home_team_history_opponent_goal + self.away_team_history_opponent_goal].astype('int64')
        assert self.dataset[
                   self.home_team_history_opponent_goal + self.away_team_history_opponent_goal].isna().sum().sum() == 0

    def fill_na_rating_team(self, to_log=True, standardization=False):
        """
        Filling the NA-values with mean value per team
        to_log:[True, False] - convert to type log + 1
        standardization:[True, False] - standardization witk StandardScaler()
        """

        columns = [f'rating_{i}' for i in range(1, 11)]
        split_index = self.dataset.shape[0]

        home_rating = self.dataset[['home_team_name'] + self.home_team_history_rating].copy()
        # home_rating['tag'] = 'home'
        home_rating.rename(columns={i: j for i, j in zip(self.home_team_history_rating, columns)}, inplace=True)
        home_rating.rename(columns={'home_team_name': 'team_name'}, inplace=True)
        home_rating.reset_index(drop=True, inplace=True)
        away_rating = self.dataset[['away_team_name'] + self.away_team_history_rating].copy()
        # away_rating['tag'] = 'away'
        away_rating.rename(columns={i: j for i, j in zip(self.away_team_history_rating, columns)}, inplace=True)
        away_rating.rename(columns={'away_team_name': 'team_name'}, inplace=True)
        away_rating.reset_index(drop=True, inplace=True)

        all_rating = pd.concat([home_rating, away_rating], axis=0)
        all_rating['mean'] = all_rating[columns].mean(axis=1)
        maping_rating = all_rating[~all_rating['mean'].isna()].pivot_table(index='team_name', values='mean')
        mean_rating = all_rating[columns].mean().mean()
        all_rating.set_index('team_name', inplace=True)

        list_na = {}
        for i in all_rating[all_rating['rating_1'].isna()].index:
            if i in maping_rating.index:
                list_na[i] = float(maping_rating.loc[i])
            else:
                list_na[i] = mean_rating

        all_rating['rating_1'] = all_rating['rating_1'].fillna(list_na)
        self.dataset['home_team_history_rating_1'] = list(all_rating.iloc[:split_index, :]['rating_1'])
        self.dataset['away_team_history_rating_1'] = list(all_rating.iloc[split_index:, :]['rating_1'])
        [self.dataset[i].fillna(self.dataset['home_team_history_rating_1'], inplace=True) for i in
         self.home_team_history_rating]
        [self.dataset[i].fillna(self.dataset['away_team_history_rating_1'], inplace=True) for i in
         self.away_team_history_rating]
        history_rating = self.home_team_history_rating + self.away_team_history_rating
        # to log
        if to_log:
            self.dataset[history_rating] = np.log(self.dataset[history_rating] + 1)
        # self.dataset[history_rating] = round(self.dataset[history_rating],15)
        # standardization
        if standardization:
            scaler = StandardScaler()
            self.dataset[history_rating] = scaler.fit_transform(self.dataset[history_rating])
        assert self.dataset[history_rating].isna().sum().sum() == 0

    def fill_na_rating_team_opponent(self, to_log=True, standardization=False):
        """
        Filling the NA-values with mean value per team
        to_log:[True, False] - convert to type log + 1
        standardization:[True, False] - standardization witk StandardScaler()
        """
        columns = [f'rating_{i}' for i in range(1, 11)]
        split_index = self.dataset.shape[0]

        home_rating = self.dataset[['home_team_name'] + self.home_team_history_opponent_rating].copy()
        # home_rating['tag'] = 'home'
        home_rating.rename(columns={i: j for i, j in zip(self.home_team_history_rating, columns)}, inplace=True)
        home_rating.rename(columns={'home_team_name': 'team_name'}, inplace=True)
        home_rating.reset_index(drop=True, inplace=True)
        away_rating = self.dataset[['away_team_name'] + self.away_team_history_opponent_rating].copy()
        # away_rating['tag'] = 'away'
        away_rating.rename(columns={i: j for i, j in zip(self.away_team_history_opponent_rating, columns)},
                           inplace=True)
        away_rating.rename(columns={'away_team_name': 'team_name'}, inplace=True)
        away_rating.reset_index(drop=True, inplace=True)

        all_rating = pd.concat([home_rating, away_rating], axis=0)
        all_rating['mean'] = all_rating[columns].mean(axis=1)
        maping_rating = all_rating[~all_rating['mean'].isna()].pivot_table(index='team_name', values='mean')
        mean_rating = all_rating[columns].mean().mean()
        all_rating.set_index('team_name', inplace=True)

        list_na = {}
        for i in all_rating[all_rating['rating_1'].isna()].index:
            if i in maping_rating.index:
                list_na[i] = float(maping_rating.loc[i])
            else:
                list_na[i] = mean_rating

        all_rating['rating_1'] = all_rating['rating_1'].fillna(list_na)
        self.dataset['home_team_history_opponent_rating_1'] = list(all_rating.iloc[:split_index, :]['rating_1'])
        self.dataset['away_team_history_opponent_rating_1'] = list(all_rating.iloc[split_index:, :]['rating_1'])
        [self.dataset[i].fillna(self.dataset['home_team_history_opponent_rating_1'], inplace=True) for i in
         self.home_team_history_opponent_rating]
        [self.dataset[i].fillna(self.dataset['away_team_history_opponent_rating_1'], inplace=True) for i in
         self.away_team_history_opponent_rating]
        history_rating = self.home_team_history_opponent_rating + self.away_team_history_opponent_rating
        # to log
        if to_log:
            self.dataset[history_rating] = np.log(self.dataset[history_rating] + 1)
        # self.dataset[history_rating] = round(self.dataset[history_rating],15)
        # standardization
        if standardization:
            scaler = StandardScaler()
            self.dataset[history_rating] = scaler.fit_transform(self.dataset[history_rating])
        assert self.dataset[history_rating].isna().sum().sum() == 0

    def fill_na_league(self, astype_int=True):
        """
        Filling NA-values with the previous data-values
        astype_int:[True, False] - convert to type 'int64'
        """
        history_league = self.home_team_history_league + self.away_team_history_league
        for num, i in enumerate(history_league):
            if num == 0 or num == 10:
                values_for_compl = self.dataset[self.dataset[i].isna()]['league_id']
                self.dataset[i].fillna(values_for_compl, inplace=True)
            else:
                values_for_compl = self.dataset[self.dataset[i].isna()][history_league[num - 1]]
                self.dataset[i].fillna(values_for_compl, inplace=True)
        assert self.dataset[history_league].isna().sum().sum() == 0
        if astype_int:
            self.dataset[history_league] = self.dataset[history_league].astype('int64')

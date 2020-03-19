import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt

from functions import *


class Hospitals:
    def __init__(self, beds, ic_death_rat, days_to_better, days_to_dead):
        self.ic_patients_df = pd.DataFrame()
        # columns=['status',
        #                                             'will_die',
        #                                             'init_day',
        #                                             'end_day',
        #                                             'alive'])
        self.beds = beds
        self.ic_death_rat = ic_death_rat
        self.day = 0
        self.days_to_better = days_to_better
        self.days_to_dead = days_to_dead
        self.current_ic = 0
        self.current_no_space = 0
        self.current_better = 0
        self.current_dead_from_ic = 0
        self.log_df = pd.DataFrame()
        self.will_die = False
        self.current_new_cases = 0
        self.current_new_ic = 0
        self.cummulative_cases = 0
        self.cummulative_no_space = 0

    # def ic_current_len(self):
    #     for entry in self.ic_patients:
    #         if self.ic_patients['status'] == 'in_ic':

    def new_patients(self, new_cases):
        self.current_new_cases = new_cases
        # for i in range(new_cases):
        #     self.generate_patient()

        self.generate_all_patients(new_cases)

    def generate_all_patients(self, new_cases):
        free_beds = self.beds - self.current_ic
        placeble_patients = min(free_beds, new_cases)

        if free_beds != 0:
            self.generate_placeble_patients(placeble_patients)

        self.generate_unplaceble_patients(max(0, new_cases - placeble_patients))

    def generate_placeble_patients(self, placeble_patients):
        # to_die_patients = int(round(placeble_patients / 2 + 0.1)) if true_or_false(0.5) else int(
        #     round(placeble_patients / 2 - 0.1))
        to_die_patients = len([1 for i in range(placeble_patients) if chance_that_true(self.ic_death_rat)])
        to_live_patients = placeble_patients - to_die_patients

        dict_die = {'status': ['in_ic' for i in range(to_die_patients)],
                    'will_die': [True for i in range(to_die_patients)],
                    'init_day': [self.day for i in range(to_die_patients)],
                    'end_day': [self.day + random_duration(average=self.days_to_dead) for i in
                                range(to_die_patients)],
                    'alive': [True for i in range(to_die_patients)]}

        self.ic_patients_df = self.ic_patients_df.append(pd.DataFrame.from_dict(dict_die, orient='index').transpose(),
                                                         ignore_index=True)

        dict_live = {'status': ['in_ic' for i in range(to_live_patients)],
                     'will_die': [False for i in range(to_live_patients)],
                     'init_day': [self.day for i in range(to_live_patients)],
                     'end_day': [self.day + random_duration(average=self.days_to_better) for i in
                                 range(to_live_patients)],
                     'alive': [True for i in range(to_live_patients)]}
        # self.ic_patients_df = self.ic_patients_df.append({'status': ['in_ic' for i in range(to_live_patients)],
        #                             'will_die': [False for i in range(to_live_patients)],
        #                             'init_day': [self.day for i in range(to_live_patients)],
        #                             'end_day': [self.day + random_duration(average=self.days_to_better) for i in
        #                                         range(to_live_patients)],
        #                             'alive': [True for i in range(to_live_patients)]}, ignore_index=True)

        self.ic_patients_df = self.ic_patients_df.append(pd.DataFrame.from_dict(dict_live, orient='index').transpose(),
                                                         ignore_index=True)

        self.current_ic += to_live_patients + to_die_patients
        self.current_new_ic += to_live_patients + to_die_patients

    def generate_unplaceble_patients(self, immediate_deaths):  # why not from dict etc?
        dict_imm = {'status': ['immediate_death' for i in range(immediate_deaths)],
                    'will_die': [None for i in range(immediate_deaths)],
                    'init_day': [self.day for i in range(immediate_deaths)],
                    'end_day': [None for i in
                                range(immediate_deaths)],
                    'alive': [False for i in range(immediate_deaths)]}

        self.ic_patients_df = self.ic_patients_df.append(pd.DataFrame.from_dict(dict_imm, orient='index').transpose(),
                                                         ignore_index=True)

        self.current_no_space += immediate_deaths

    # def generate_patient(self):
    #     if not len(self.ic_patients_df) or len(
    #             self.ic_patients_df[self.ic_patients_df['status'] == 'in_ic']) < self.beds:
    #
    #         # will_die = true_or_false(self.ic_death_rat)
    #         will_die = bool(self.will_die)
    #         self.will_die = ~self.will_die
    #
    #         new_patient = {'status': 'in_ic',
    #                        'will_die': will_die,
    #                        'init_day': self.day,
    #                        'end_day': self.day + random_duration(
    #                            average=self.days_to_dead) if will_die else self.day + random_duration(
    #                            self.days_to_better),
    #                        'alive': True}
    #         self.current_ic += 1
    #         self.current_new_ic += 1
    #
    #         # if len(self.ic_patients_df):
    #         #     print(len(self.ic_patients_df['status'] == 'in_ic'))
    #     else:
    #         self.current_imm_dead += 1
    #         # will_die = true_or_false(self.ic_death_rat)
    #         new_patient = {'status': 'immediate_death',
    #                        'will_die': None,
    #                        'init_day': self.day,
    #                        'end_day': None,
    #                        'alive': False}
    #
    #     self.ic_patients_df = self.ic_patients_df.append(new_patient, ignore_index=True)

    def leave_hospital(self):
        # if self.day == 5:
        #     print('sdf')
        if self.day == 80:
            print('sdf')
        # if self.day == 15:
        #     print('sdf')
        # if self.day == 20:
        #     print('sdf')
        # self.ic_patients_df[][['status', 'alive']] = ['dead_from_ic', False]

        if len(self.ic_patients_df):
            self.current_dead_from_ic = len(self.ic_patients_df.loc[
                                                (self.ic_patients_df['status'] == 'in_ic') & (
                                                        self.ic_patients_df['will_die'] == True) & (
                                                        self.ic_patients_df['end_day'] == self.day)])

            self.current_better = len(self.ic_patients_df.loc[
                                          (self.ic_patients_df['status'] == 'in_ic') & (
                                                  self.ic_patients_df['will_die'] == False) & (
                                                  self.ic_patients_df['end_day'] == self.day)])

            self.current_ic -= self.current_better + self.current_dead_from_ic

            self.ic_patients_df.loc[
                (self.ic_patients_df['status'] == 'in_ic') & (self.ic_patients_df['will_die'] == True) & (
                        self.ic_patients_df['end_day'] == self.day), ['status', 'alive']] = ['dead_from_ic', False]

            self.ic_patients_df.loc[
                (self.ic_patients_df['status'] == 'in_ic') & (self.ic_patients_df['will_die'] == False) & (
                        self.ic_patients_df['end_day'] == self.day), ['status', 'alive']] = ['better_from_ic', True]

        # self.ic_patients_df[(self.ic_patients_df['status'] == 'in_ic') & (self.ic_patients_df['will_die'] == False) & (
        #         self.ic_patients_df['end_day'] == self.day)][['status', 'alive']] = ['better_from_ic', True]

    def add_day(self):
        self.day += 1
        self.cummulative_cases += self.current_new_cases
        self.cummulative_no_space += self.current_no_space
        self.current_no_space = 0
        self.current_new_ic = 0
        # print(f'day {self.day}      {self.current_new_cases}    {self.current_ic}  }')
        print(f'day {self.day}')

    def log_day(self):
        log_dict = {
            'current_ic': self.current_ic,
            'no_space_per_day': self.current_no_space,
            'current_better': self.current_better,
            'current_dead_from_ic': self.current_dead_from_ic,
            'new_cases': self.current_new_cases,
            'cummulative_cases': self.cummulative_cases,
            'cummulative_no_space': self.cummulative_no_space
        }
        self.log_df = self.log_df.append(log_dict, ignore_index=True)

        # if self.day % 10 == 0:
        #
        #     # plt.clf()
        #     for column in hospitals.log_df.columns:
        #         plt.plot(np.arange(len(hospitals.log_df)), hospitals.log_df[column],
        #                  linewidth=2, label=column)
        #     plt.legend()
        #     plt.grid(which='minor')
        #     plt.show()
        #     # plt.savefig('foo.png')

    # def summarise(self):
    def plot_log(self, log=True, map_days=False, start_day='21-02-2020', day_zero=dt.date.today()):
        # if not map_days:
        fig, ax = plt.subplots(dpi=300)
        days = np.arange(self.day)
        if map_days:
            days = days - (pd.to_datetime(day_zero) - pd.to_datetime(start_day)).days

        for column in self.log_df.columns:
            ax.plot(days, self.log_df[column],    linewidth=2, label=column)
        if log:
            ax.set_yscale('log')
        plt.legend()
        ax.set_xticks(days, minor=True)
        ax.grid(which='both')
        # fig.autofmt_xdate()
        plt.show()


        # fig, ax = plt.subplots(dpi=300)
        # for scenario in sequence:
        #     # plot_days_first = sequence[scenario][1]
        #     predicted_ic_df = plot_future(df_ic, pivots=sequence[scenario])
        #     predicted_ic_df.to_excel('test.xlsx')
        #
        #     ax.plot(np.array(predicted_ic_df['date']), np.array(predicted_ic_df['number']))
        #
        #     # ax.set_xticks(ax.get_xticks()[::3])
        # ax.set_ylabel('Total IC cases NL')
        # ax.set_yscale('log')
        # ax.grid('both')
        # fig.autofmt_xdate()
        # plt.show()
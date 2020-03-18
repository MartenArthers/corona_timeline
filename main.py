import pandas as pd
import random
import numpy as np

import matplotlib.pyplot as plt

mu, sigma = 0, 1  # mean and standard deviation
# s = np.random.normal(mu, sigma, 1000)

# count, bins, ignored = plt.hist(s, 30, density=True)

days = 200
beds = 2000

ic_death_rat = 0.5
days_to_better = 10
days_to_dead = 5

people = 17000000
cont = 0.5
hosp = 0.02
ic = 0.2
ic_patients = people * cont * hosp * ic
print(f'IC patients = {ic_patients}')

sigma_multiplier = 3
x = np.linspace(-sigma_multiplier * sigma, sigma_multiplier * sigma, days)
y = np.exp(- (x - mu) ** 2 / (2 * sigma ** 2)) ** 2
y_sum = sum(y)
factor = ic_patients / y_sum
norm_y = factor * y
y_round = np.round(norm_y).astype(int)
# plt.plot(np.arange(days), y_round,
#          linewidth=2, color='r', label='label')
#
# plt.legend()
# plt.show()


print(f'simulated IC patients={sum(y_round)}')


#
# ic_deaths = 0.5
# tt_death = 5  # days
# tt_better = 10  # days
#
# beds = 2000


def true_or_false(probability):
    return random.random() < probability


def random_duration(average):
    sigma = 0.2 * average
    s = max(round(np.random.normal(average, sigma)), 1)
    return s


a = random_duration(10)


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
        self.current_imm_dead = 0
        self.current_better = 0
        self.current_dead_from_ic = 0
        self.log_df = pd.DataFrame()
        self.will_die = False
        self.current_new_cases = 0
        self.current_new_ic = 0

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
        to_die_patients = int(round(placeble_patients / 2 + 0.1)) if true_or_false(0.5) else int(
            round(placeble_patients / 2 - 0.1))
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

    def generate_unplaceble_patients(self, immediate_deaths):
        self.ic_patients_df = self.ic_patients_df.append(
            {'status': ['immediate_death' for i in range(immediate_deaths)],
             'will_die': [None for i in range(immediate_deaths)],
             'init_day': [self.day for i in range(immediate_deaths)],
             'end_day': [None for i in
                         range(immediate_deaths)],
             'alive': [False for i in range(immediate_deaths)]}, ignore_index=True)

        self.current_imm_dead += immediate_deaths

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
        self.current_imm_dead = 0
        self.current_new_ic = 0
        print(self.day)

    def log_day(self):
        log_dict = {
            'current_ic': self.current_ic,
            'current_imm_dead': self.current_imm_dead,
            'current_better': self.current_better,
            'current_dead_from_ic': self.current_dead_from_ic,
            'new_cases': self.current_new_cases
        }
        self.log_df = self.log_df.append(log_dict, ignore_index=True)

        if self.day % 10 == 0:

            # plt.clf()
            for column in hospitals.log_df.columns:
                plt.plot(np.arange(len(hospitals.log_df)), hospitals.log_df[column],
                         linewidth=2, label=column)
            plt.legend()
            plt.grid(which='minor')
            plt.show()
            # plt.savefig('foo.png')


contag_list = y_round

hospitals = Hospitals(beds=beds, ic_death_rat=ic_death_rat, days_to_better=days_to_better, days_to_dead=days_to_dead)

for new_cases in contag_list:
    hospitals.leave_hospital()
    hospitals.new_patients(new_cases)
    hospitals.log_day()
    hospitals.add_day()

for column in hospitals.log_df.columns:
    plt.plot(np.arange(days), hospitals.log_df[column],
             linewidth=2, label=column)
plt.legend()
plt.grid(which='both')
plt.show()

print('break')

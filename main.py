import pandas as pd
import random
import numpy as np

import matplotlib.pyplot as plt

mu, sigma = 0, 1  # mean and standard deviation
# s = np.random.normal(mu, sigma, 1000)

# count, bins, ignored = plt.hist(s, 30, density=True)

days = 25

people = 170000
cont = 0.5
hosp = 0.2
ic = 0.2
ic_patients = people * cont * hosp * ic
print(f'IC patients = {ic_patients}')

sigma_multiplier = 3
x = np.linspace(-sigma_multiplier * sigma, sigma_multiplier * sigma, days)
y = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))
y_sum = sum(y)
factor = ic_patients / y_sum
norm_y = factor * y
y_round = np.round(norm_y).astype(int)
plt.plot(np.arange(days), y_round,
         linewidth=2, color='r', label='label')

plt.legend()
plt.show()

print(f'simulated IC patients={sum(y_round)}')


#
# ic_deaths = 0.5
# tt_death = 5  # days
# tt_better = 10  # days
#
# beds = 2000


def true_or_false(probability):
    return random.random() < probability


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

    # def ic_current_len(self):
    #     for entry in self.ic_patients:
    #         if self.ic_patients['status'] == 'in_ic':

    def new_patients(self, new_cases):
        for i in range(new_cases):
            self.generate_patient()

    def generate_patient(self):
        if not len(self.ic_patients_df) or len(
                self.ic_patients_df[self.ic_patients_df['status'] == 'in_ic']) < self.beds:

            # will_die = true_or_false(self.ic_death_rat)
            will_die = self.will_die
            self.will_die = ~self.will_die

            new_patient = {'status': 'in_ic',
                           'will_die': will_die,
                           'init_day': self.day,
                           'end_day': self.day + self.days_to_dead if will_die else self.day + self.days_to_better,
                           'alive': True}
            self.current_ic += 1
            # if len(self.ic_patients_df):
            #     print(len(self.ic_patients_df['status'] == 'in_ic'))
        else:
            self.current_imm_dead += 1
            # will_die = true_or_false(self.ic_death_rat)
            new_patient = {'status': 'immediate_death',
                           'will_die': None,
                           'init_day': self.day,
                           'end_day': None,
                           'alive': False}

        self.ic_patients_df = self.ic_patients_df.append(new_patient, ignore_index=True)

    def leave_hospital(self):
        # if self.day == 5:
        #     print('sdf')
        # if self.day == 10:
        #     print('sdf')
        # if self.day == 15:
        #     print('sdf')
        # if self.day == 20:
        #     print('sdf')
        # self.ic_patients_df[][['status', 'alive']] = ['dead_from_ic', False]

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
        print(self.day)

    def log_day(self):
        log_dict = {
            'current_ic': self.current_ic,
            'current_imm_dead': self.current_imm_dead,
            'current_better': self.current_better,
            'current_dead_from_ic': self.current_dead_from_ic,
        }
        self.log_df = self.log_df.append(log_dict, ignore_index=True)


contag_list = y_round

hospitals = Hospitals(beds=500, ic_death_rat=0.5, days_to_better=10, days_to_dead=5)

for new_cases in contag_list:
    hospitals.new_patients(new_cases)
    hospitals.leave_hospital()
    hospitals.log_day()
    hospitals.add_day()

# plt.plot(np.arange(days), y_round,
#          linewidth=2, color='r')
plt.plot(np.arange(days), hospitals.log_df['current_ic'],
         linewidth=2, label='current_ic')
plt.plot(np.arange(days), hospitals.log_df['current_imm_dead'],
         linewidth=2, label='current_imm_dead')
plt.plot(np.arange(days), hospitals.log_df['current_better'],
         linewidth=2, label='current_better')
plt.plot(np.arange(days), hospitals.log_df['current_dead_from_ic'],
         linewidth=2, label='current_dead_from_ic')
plt.legend()
plt.show()

print('break')

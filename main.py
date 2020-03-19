import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from classes import *

beds = 2000
ic_death_rat = 0.1
days_to_better = 15
days_to_dead = 10

## option 1: real and predicted data
y_round, days = list_of_real_predicted_new_cases()

# ## option2: fabricated inputs
# days = 120
# people = 17000000
# cont = 0.5
# hosp = 0.02
# ic = 0.2
# ic_patients = people * cont * hosp * ic
# # y_round = list_of_normal_new_cases(ic_patients=ic_patients, days=days, mu=0, sigma=1, sigma_multiplier=3)
# y_round = list_of_logistic_new_cases(ic_patients=ic_patients, days=days, mu=0, sigma=1, sigma_multiplier=3)

hospitals = Hospitals(beds=beds, ic_death_rat=ic_death_rat, days_to_better=days_to_better, days_to_dead=days_to_dead)

for new_cases in y_round:
    hospitals.leave_hospital()
    hospitals.new_patients(new_cases)
    hospitals.add_day()
    hospitals.log_day()


hospitals.plot_log(log=True, map_days=True, start_day='21-02-2020', day_zero=dt.date.today())

# hospitals.summarise()


print('break')

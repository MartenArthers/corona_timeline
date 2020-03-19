import pandas as pd
import random
import numpy as np
import datetime as dt


def chance_that_true(probability):
    return random.random() < probability


def random_duration(average):
    sigma = 0.00002 * average
    s = max(round(np.random.normal(average, sigma)), 1)
    return s


def list_of_normal_new_cases(ic_patients, days, mu=0, sigma=1, sigma_multiplier=3):
    print(f'IC patients = {ic_patients}')
    effective_sigma = sigma * sigma_multiplier
    x = np.linspace(-effective_sigma, effective_sigma, days)
    y = np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))
    y_sum = sum(y)
    factor = ic_patients / y_sum
    norm_y = factor * y
    y_round = np.round(norm_y).astype(int)
    print(f'simulated IC patients={sum(y_round)}')
    # plt.plot(np.arange(days), y_round,
    #          linewidth=2, color='r', label='label')
    #
    # plt.legend()
    # plt.show()

    return y_round


def list_of_logistic_new_cases(ic_patients, days, mu=0, sigma=1, sigma_multiplier=3):
    print(f'IC patients = {ic_patients}')
    effective_sigma = 2 * sigma * sigma_multiplier
    x = np.linspace(-effective_sigma, effective_sigma, days)
    y = np.exp(- (x - mu) / sigma) / (1 + np.exp(- (x - mu) / sigma)) ** 2
    y_sum = sum(y)
    factor = ic_patients / y_sum
    norm_y = factor * y
    y_round = np.round(norm_y).astype(int)
    print(f'simulated IC patients={sum(y_round)}')
    # plt.plot(np.arange(days), y_round,
    #          linewidth=2, color='r', label='label')
    #
    # plt.legend()
    # plt.show()

    return y_round

def list_of_real_predicted_new_cases():
    worst = 0.11
    medium = worst / 2
    best = worst / 3
    plot_days = 50
    scenarios = {'worst': [{'duration': 10, 'growth': 10 ** worst}, {'duration': plot_days - 10, 'growth': 10 ** worst}],
                 'medium': [{'duration': 5, 'growth': 10 ** worst}, {'duration': plot_days - 5, 'growth': 10 ** medium}],
                 'best': [{'duration': 3, 'growth': 10 ** worst}, {'duration': plot_days - 3, 'growth': 10 ** best}]}
    actual_ic_df = fetch_actual_ic_df()
    predicted_ic_df = plot_future(actual_ic_df, pivots=scenarios['best'])
    predicted_ic_df['new_ic'] = predicted_ic_df['number'].diff().fillna(0)
    return predicted_ic_df['new_ic'].astype(int), len(predicted_ic_df['new_ic'])


def fetch_actual_ic_df():
    df_ic = pd.read_excel('ic-data.xlsx')
    # df_ic['new_ic'] = df_ic['op ic (cummulatief)'].diff().fillna(0)
    df_ic['date'] = pd.to_datetime(df_ic['date'])
    df_ic = df_ic[['op ic (cummulatief)', 'date']]
    df_ic.columns = ['number', 'date']
    return df_ic


def plot_future(df_ic, pivots=[{'duration': 10, 'growth': 1.25},
                               {'duration': 20, 'growth': 1.1}]):  # df with at least columns ['number','date']
    df_ic['date'] = pd.to_datetime(df_ic['date'])
    days = len(df_ic['date'])
    first_date = df_ic.iloc[0]['date']
    total_predicted_days = 0
    for pivot_dict in pivots:
        last_value = df_ic.iloc[-1]['number']
        new_g = pivot_dict['growth']
        new_values = [last_value * new_g ** (i + 1) for i in range(pivot_dict['duration'])]
        total_predicted_days += pivot_dict['duration']
        new_values_dict = {'number': new_values}

        df_ic = df_ic.append(pd.DataFrame.from_dict(new_values_dict, orient='index').transpose())

    df_ic['date'] = pd.date_range(start=first_date, end=first_date + dt.timedelta(days=days + total_predicted_days - 1))

    return df_ic


# first = 3

# sequence = {'worst': [{'duration': 10, 'growth': 10 ** worst}, {'duration': plot_days - 10, 'growth': 10 ** worst}],
#             'medium': [{'duration': 5, 'growth': 10 ** worst}, {'duration': plot_days - 5, 'growth': 10 ** medium}],
#             'best': [{'duration': 3, 'growth': 10 ** worst}, {'duration': plot_days - 3, 'growth': 10 ** best}]}

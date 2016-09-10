#!/usr/bin/env python

import os
import time

import pandas as pd

import badgets as bg

script_dir = os.path.dirname(os.path.realpath(__file__))
initial_budgets = pd.read_json('{}/json/budgets.json'.format(script_dir),
                               orient='index').loc[:, 'budget'].to_dict()

# to float
for adv in initial_budgets:
    initial_budgets[adv] = float(initial_budgets[adv])

advertisers = [
    'adv_01',
    'adv_02',
    'adv_03',
    'adv_04',
    'adv_05',
    'adv_06',
    'adv_07',
    'adv_08',
    'adv_09',
    'adv_10',
    'adv_11',
    'adv_12',
    'adv_13',
    'adv_14',
    'adv_15',
    'adv_16',
    'adv_17',
    'adv_18',
    'adv_19',
    'adv_20',
]

bg.connect()

while True:
    time.sleep(1)

    current_budgets = bg.get_budgets()

    print '*' * 40
    print time.ctime()
    for adv in advertisers:
        ratio = 100 * current_budgets[adv] / initial_budgets[adv]
        print '{}: {:11.2f} / {:11.2f} ({:5.1f}%)'.format(
            adv, current_budgets[adv], initial_budgets[adv], ratio)

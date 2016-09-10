#!/usr/bin/env python

import sys

import badgets as bg

bg.connect()
budgets = bg.get_budgets()

if len(sys.argv) == 2:
    for adv in budgets:
        budgets[adv] = float(sys.argv[1])
else:
    budgets[sys.argv[1]] = float(sys.argv[2])

bg.set_budgets(budgets)

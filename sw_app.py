#!/bin/python3

import sw_history
import sw_setup
import sw_stock
import sw_study

while True:
    print('=' * 60)
    print('SWING APP')
    print('-' * 60)
    print('1 - update ALL')
    print('2 - update "200,21,250000,5"')
    print('3 - setup CRSI')
    print('0 - exit')
    print('=' * 60)
    print('enter choice #', end=':')
    script = int(input())

    if script == 1 or script == 2:
        # ---------------------------------------------------------------------------
        # update
        # ---------------------------------------------------------------------------
        stock = sw_stock.Stock()
        history = sw_history.History()
        study = sw_study.Study(history)
        setup = sw_setup.Setup(history, study)
        selected = stock.stocks() if script == 1 else stock.selected(200, 21, 250000, 5)
        history.update(selected)
        study.update(selected)

    elif script == 3:
        # ---------------------------------------------------------------------------
        # setup CRSI
        # ---------------------------------------------------------------------------
        date = input('enter pre-enter date [YYYY-MM-DD]:')
        stock = sw_stock.Stock()
        history = sw_history.History()
        study = sw_study.Study(history)
        setup = sw_setup.Setup(history, study)
        selected = stock.selected(200, 21, 250000, 5)
        setup.setup_crsi(selected, date)

    elif script == 0:
        # ---------------------------------------------------------------------------
        # exit
        # ---------------------------------------------------------------------------
        break

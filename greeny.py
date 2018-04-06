#!/bin/python3

import time
import daily
import stock

while True:
    print('=' * 80)
    print('GREENY')
    print('-' * 80)
    print('1 - full daily download and update (once a quarter)')
    print('2 - full daily update (once a week)')
    print('3 - selected daily update (daily)')
    print('0 - exit')
    print('=' * 80)
    print('enter choice #', end=':')
    script = int(input())

    if script == 1:
        # ---------------------------------------------------------------------------
        # full daily download and update (once a quarter)
        # ---------------------------------------------------------------------------
        started = time.time()
        history = daily.History()
        study = daily.Study()
        symbols = stock.Symbol().symbols()
        fundamentals = stock.Fundamentals()
        history.download(symbols, False)
        history.update(symbols)
        study.update(symbols)
        fundamentals.update()
        print(time.strftime('"full daily download and update" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 2:
        # ---------------------------------------------------------------------------
        # full daily update (once a week)
        # ---------------------------------------------------------------------------
        started = time.time()
        history = daily.History()
        study = daily.Study()
        symbols = stock.Symbol().symbols()
        history.update(symbols)
        study.update(symbols)
        print(time.strftime('"full daily update" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 3:
        # ---------------------------------------------------------------------------
        # selected daily update (daily)
        # ---------------------------------------------------------------------------
        selection = input('enter selection to update:')
        started = time.time()
        history = daily.History()
        study = daily.Study()
        symbols = stock.Symbol().symbols(selection)
        history.update(symbols)
        study.update(symbols)
        print(time.strftime('"selected daily update" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 0:
        # ---------------------------------------------------------------------------
        # exit
        # ---------------------------------------------------------------------------
        break

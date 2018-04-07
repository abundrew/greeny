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
        if input('full daily download and update. start? [Y/N]').upper() == 'Y':
            started = time.time()
            history = daily.History()
            symbols = stock.Symbol().symbols()
            history.download(symbols, False)
            history.update(symbols)
            daily.Study().update(symbols)
            stock.Fundamentals().update()
            stock.Selection().update()
            print(time.strftime('"full daily download and update" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 2:
        # ---------------------------------------------------------------------------
        # full daily update (once a week)
        # ---------------------------------------------------------------------------
        if input('full daily update. start? [Y/N]').upper() == 'Y':
            started = time.time()
            symbols = stock.Symbol().symbols()
            daily.History().update(symbols)
            daily.Study().update(symbols)
            stock.Selection().update()
            print(time.strftime('"full daily update" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 3:
        # ---------------------------------------------------------------------------
        # selected daily update (daily)
        # ---------------------------------------------------------------------------
        selection = input('enter selection to update:').upper()
        started = time.time()
        symbols = stock.Symbol().symbols(selection)
        daily.History().update(symbols)
        daily.Study().update(symbols)
        stock.Selection().update()
        print(time.strftime('"selected daily update" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 0:
        # ---------------------------------------------------------------------------
        # exit
        # ---------------------------------------------------------------------------
        break

#!/bin/python3

import time
import daily
import stock

while True:
    print('=' * 80)
    print('GREENY')
    print('-' * 80)
    print('1 - full daily download and update (once a quarter)')
    print('2 - fundamentals update (once a quarter)')
    print('3 - full daily update (once a week)')
    print('4 - selected daily update (daily)')
    print('5 - uptrend + more $20 + liquid + crsi < 20')
    print('6 - stats')
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
        # fundamentals update (once a quarter)
        # ---------------------------------------------------------------------------
        if input('fundamentals update. start? [Y/N]').upper() == 'Y':
            started = time.time()
            stock.Fundamentals().update()
            print(time.strftime('"fundamentals update" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 3:
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

    elif script == 4:
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

    elif script == 5:
        # ---------------------------------------------------------------------------
        # uptrend + more $20 + liquid + crsi < 20
        # ---------------------------------------------------------------------------
        selected = stock.Selection().select(['UPTREND','MORE_20','LIQUID','CRSI_20'])
        print('[uptrend + more $20 + liquid + crsi < 20]:')
        print(len(selected))
        print(' '.join(selected))

    elif script == 6:
        # ---------------------------------------------------------------------------
        # stats
        # ---------------------------------------------------------------------------
        symbol = input('enter symbol:').upper()
        fundamentals = stock.Fundamentals()
        stats = fundamentals.stats(symbol)
        for key in list(stats):
            print('{} : {}'.format(key, stats[key]))

    elif script == 0:
        # ---------------------------------------------------------------------------
        # exit
        # ---------------------------------------------------------------------------
        break

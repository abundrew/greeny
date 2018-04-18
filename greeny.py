#!/bin/python3

import time
import daily
import intraday
import stock

while True:
    print('=' * 80)
    print('GREENY')
    print('-' * 80)
    print('1 - full daily download and update (once a quarter)')
    print('2 - fundamentals update (once a quarter)')
    print('3 - full daily update (once a week)')
    print('4 - full intraday update (once a week)')
    print('5 - selected daily update (daily)')
    print('6 - fixed + uptrend + more $20 + liquid + crsi < 10')
    print('7 - fixed + uptrend + more $20 + liquid + crsi < 20')
    print('8 - fixed + uptrend + more $20 + liquid + crsi < 25')
    print('9 - stats')
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
            history.download(symbols) #,true
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
        # full intraday update (once a week)
        # ---------------------------------------------------------------------------
        if input('full intraday update. start? [Y/N]').upper() == 'Y':
            started = time.time()
            symbols = stock.Symbol().symbols()
            history = intraday.History()
            history.download(symbols)
            history.update(symbols)
            print(time.strftime('"full intraday update" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 5:
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

    elif script == 6:
        # ---------------------------------------------------------------------------
        # fixed + uptrend + more $20 + liquid + crsi < 10
        # ---------------------------------------------------------------------------
        selected = stock.Selection().select(['FIXED','UPTREND','MORE_20','LIQUID','CRSI_10'])
        print('[fixed + uptrend + more $20 + liquid + crsi < 10]:')
        print(len(selected))
        print(' '.join(selected))

    elif script == 7:
        # ---------------------------------------------------------------------------
        # fixed + uptrend + more $20 + liquid + crsi < 20
        # ---------------------------------------------------------------------------
        selected = stock.Selection().select(['FIXED','UPTREND','MORE_20','LIQUID','CRSI_20'])
        print('[fixed + uptrend + more $20 + liquid + crsi < 20]:')
        print(len(selected))
        print(' '.join(selected))

    elif script == 8:
        # ---------------------------------------------------------------------------
        # fixed + uptrend + more $20 + liquid + crsi < 25
        # ---------------------------------------------------------------------------
        selected = stock.Selection().select(['FIXED','UPTREND','MORE_20','LIQUID','CRSI_25'])
        print('[fixed + uptrend + more $20 + liquid + crsi < 25]:')
        print(len(selected))
        print(' '.join(selected))

    elif script == 9:
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

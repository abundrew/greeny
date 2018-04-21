#!/bin/python3

import time
import pandas as pd
import config
import daily
import stock

while True:
    print('=' * 80)
    print('$$$$$ GREEDY $$$$$')
    print('-' * 80)
    print('1 - help')
    print('2 - update fundamentals (once in a while)')
    print('3 - download missing daily files')
    print('4 - update daily files (with US Equities file)')
    print('5 - update studies')
    print('6 - update selections')
    print('7 - get cross-selection')
    print('8 - get stats')
    print('0 - exit')
    print('=' * 80)
    print('enter choice #', end=':')
    script = int(input())

    if script == 1:
        # ---------------------------------------------------------------------------
        # help
        # ---------------------------------------------------------------------------
        print('A. Download fundamentals')
        print('B. Download daily files')
        print('C. Download US Equities')
        print('   at http://eoddata.com/myaccount/accountdetails.aspx')
        print("   to '../data/daily/eoddata/USE_{}.txt'")
        print("   Skip holidays")
        print("   (http://www.theholidayschedule.com/nyse-holidays.php)")
        print('D. Update symbols.csv with symbols from US Equities file')
        print("   Replace '^([^,]+)(.*)$' with '\\1'")
        print('E. Update daily files using US Equities files by date')
        print('F. Update study files')
        print('G. Update selections')
        print('H. Get cross-selection')
        print('I. Get stats')

    elif script == 2:
        # ---------------------------------------------------------------------------
        # update fundamentals (once in a while)
        # ---------------------------------------------------------------------------
        if input('update fundamentals. start? [Y/N]').upper() == 'Y':
            started = time.time()
            stock.Fundamentals().update()
            print(time.strftime('"update fundamentals" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 3:
        # ---------------------------------------------------------------------------
        # download missing daily files
        # ---------------------------------------------------------------------------
        if input('download missing daily files. start? [Y/N]').upper() == 'Y':
            started = time.time()
            history = daily.History()
            symbols = stock.Symbol().symbols()
            history.download(symbols)
            print(time.strftime('"download missing daily files" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 4:
        # ---------------------------------------------------------------------------
        # update daily files (with US Equities file)
        # ---------------------------------------------------------------------------
        if input('update daily files (with US Equities file). start? [Y/N]').upper() == 'Y':
            print('start date [YYYY-MM-DD]', end=':')
            start_date = input()
            print('end date [YYYY-MM-DD]', end=':')
            end_date = input()
            started = time.time()
            history = daily.History()
            symbols = stock.Symbol().symbols()
            for di in pd.date_range(start_date, end_date):
                eoddate = str(di)[:10]
                print(eoddate)
                fname = config.FORMAT_DAILY_EODDATA.format(eoddate[:4] + eoddate[5:7] + eoddate[8:])
                history.update_from_file(symbols, fname)
            print(time.strftime('"update daily files (with US Equities file)" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 5:
        # ---------------------------------------------------------------------------
        # update studies
        # ---------------------------------------------------------------------------
        if input('update studies. start? [Y/N]').upper() == 'Y':
            started = time.time()
            symbols = stock.Symbol().symbols()
            daily.Study().update(symbols)
            print(time.strftime('"update studies" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 6:
        # ---------------------------------------------------------------------------
        # update selections
        # ---------------------------------------------------------------------------
        started = time.time()
        stock.Selection().update()
        print(time.strftime('"update selections" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 7:
        # ---------------------------------------------------------------------------
        # get cross-selection
        # ---------------------------------------------------------------------------
        print ('1. uptrend + more $20 + liquid + crsi < 10')
        print ('2. uptrend + more $20 + liquid + crsi < 20')
        print ('3. uptrend + more $20 + liquid + crsi < 25')
        print('enter choice #', end=':')
        choice = int(input())

        if choice == 1:
            # ---------------------------------------------------------------------------
            # uptrend + more $20 + liquid + crsi < 10
            # ---------------------------------------------------------------------------
            selected = stock.Selection().select(['UPTREND','MORE_20','LIQUID','CRSI_10'])
            print('[uptrend + more $20 + liquid + crsi < 10]:')
            print(len(selected))
            print(' '.join(selected))

        elif choice == 2:
            # ---------------------------------------------------------------------------
            # uptrend + more $20 + liquid + crsi < 20
            # ---------------------------------------------------------------------------
            selected = stock.Selection().select(['UPTREND','MORE_20','LIQUID','CRSI_20'])
            print('[uptrend + more $20 + liquid + crsi < 20]:')
            print(len(selected))
            print(' '.join(selected))

        elif choice == 3:
            # ---------------------------------------------------------------------------
            # uptrend + more $20 + liquid + crsi < 25
            # ---------------------------------------------------------------------------
            selected = stock.Selection().select(['UPTREND','MORE_20','LIQUID','CRSI_25'])
            print('[uptrend + more $20 + liquid + crsi < 25]:')
            print(len(selected))
            print(' '.join(selected))

    elif script == 8:
        # ---------------------------------------------------------------------------
        # get stats
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

#!/bin/python3

import time
import iex_api
import sw_chart
import sw_history
import sw_setup
import sw_stock
import sw_stock_filter
import sw_study

while True:
    print('=' * 60)
    print('SWING APP')
    print('-' * 60)
    print('1 - history tail')
    print('2 - chart')
    print('3 - stats')
    print('4 - select "connors filter" stocks')
    print('5 - select "rocket" stocks')
    print('6 - update ALL')
    print('7 - update "connors filter" stocks')
    print('8 - setup CRSI')
    print('0 - exit')
    print('=' * 60)
    print('enter choice #', end=':')
    script = int(input())

    print(time.strftime('%Y-%m-%d %H:%M:%S started...', time.localtime()))

    if script == 1:
        # ---------------------------------------------------------------------------
        # history tail
        # ---------------------------------------------------------------------------
        stock = input('enter stock e.g. AAPL:')
        history = sw_history.History()
        hdf = history.to_dataframe(stock)
        print(hdf.tail())

    elif script == 2:
        # ---------------------------------------------------------------------------
        # chart
        # ---------------------------------------------------------------------------
        stock = input('enter stock e.g. AAPL:')
        sw_chart.chart(stock)

    elif script == 3:
        # ---------------------------------------------------------------------------
        # connors filter
        # ---------------------------------------------------------------------------
        stock = input('enter stock e.g. AAPL:')
        stats = iex_api.stock_stats(stock)
        if stats['success']:
            for key in stats['data']:
                print('{} : {}'.format(key, stats['data'][key]))

    elif script == 4:
        # ---------------------------------------------------------------------------
        # connors filter
        # ---------------------------------------------------------------------------
        stock = sw_stock.Stock()
        stock_filter = sw_stock_filter.StockFilter()
        selected = stock.select("connors_filter", stock_filter.connors_filter, stock.stocks())
        print('Selected: {} {} {}'.format(len(selected), ' '.join(selected[:10]), '...' if len(selected) > 10 else ''))

    elif script == 5:
        # ---------------------------------------------------------------------------
        # rocket filter
        # ---------------------------------------------------------------------------
        stock = sw_stock.Stock()
        stock_filter = sw_stock_filter.StockFilter()
        selected = stock.select("rocket", stock_filter.rocket_filter, stock.stocks())
        print('Selected: {} {} {}'.format(len(selected), ' '.join(selected[:10]), '...' if len(selected) > 10 else ''))

    elif script == 6 or script == 7:
        # ---------------------------------------------------------------------------
        # update
        # ---------------------------------------------------------------------------
        stock = sw_stock.Stock()
        history = sw_history.History()
        study = sw_study.Study(history)
        setup = sw_setup.Setup(history, study)
        selected = stock.stocks() if script == 6 else stock.select("connors_filter")
        history.update(selected)
        study.update(selected)

    elif script == 8:
        # ---------------------------------------------------------------------------
        # setup CRSI
        # ---------------------------------------------------------------------------
        date = input('enter pre-enter date [YYYY-MM-DD]:')
        stock = sw_stock.Stock()
        history = sw_history.History()
        study = sw_study.Study(history)
        setup = sw_setup.Setup(history, study)
        selected = stock.select("connors_filter")
        setup.setup_crsi(selected, date)

    elif script == 0:
        # ---------------------------------------------------------------------------
        # exit
        # ---------------------------------------------------------------------------
        break

    print(time.strftime('%Y-%m-%d %H:%M:%S finished...', time.localtime()))

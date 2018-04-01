#!/bin/python3

import time
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
    print('1 - chart')
    print('2 - select "connors filter" stocks')
    print('3 - update ALL')
    print('4 - update "connors filter" stocks')
    print('5 - setup CRSI')
    print('0 - exit')
    print('=' * 60)
    print('enter choice #', end=':')
    script = int(input())

    print(time.strftime('%Y-%m-%d %H:%M:%S started...', time.localtime()))

    if script == 1:
        # ---------------------------------------------------------------------------
        # setup CRSI
        # ---------------------------------------------------------------------------
        stock = input('enter stock e.g. AAPL:')
        sw_chart.chart(stock)

    elif script == 2:
        # ---------------------------------------------------------------------------
        # update
        # ---------------------------------------------------------------------------
        stock = sw_stock.Stock()
        stock_filter = sw_stock_filter.StockFilter()
        stock.select("connors_filter", stock_filter.connors_filter, stock.stocks())

    elif script == 3 or script == 4:
        # ---------------------------------------------------------------------------
        # update
        # ---------------------------------------------------------------------------
        stock = sw_stock.Stock()
        history = sw_history.History()
        study = sw_study.Study(history)
        setup = sw_setup.Setup(history, study)
        selected = stock.stocks() if script == 1 else stock.select("connors_filter")
        history.update(selected)
        study.update(selected)

    elif script == 5:
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

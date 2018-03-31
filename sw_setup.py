#!/bin/python3

import datetime
import sw_entry_crsi

class Setup:
    def __init__(self, history, study):
        self._history = history
        self._study = study

    def setup_crsi(self, stocks, pre_entry_date=None):
        N, W, X, Y, Z = 75, 2, 10, 5, 6
        if pre_entry_date is None:
            pre_entry_date = datetime.datetime.today().strftime('%Y-%m-%d')
        print('=' * 80)
        print('Exit CRSI > {}, limit 20 days'.format(N))
        print('Sell off %: {},  Closing range: {},  Entry CRSI: {},  Entry limit: {}'.format(W, X, Y, Z))
        print('-' * 80)
        entry = sw_entry_crsi.Entry(W, X, Y, Z)
        for stock in stocks:
            hdf = self._history.to_dataframe(stock)
            sdf = self._study.to_dataframe(stock)
            entry_price = entry.entry(hdf, sdf, pre_entry_date)
            if entry_price is None: continue
            print('{:6} - current price: {:7.2f}  entry price: {:7.2f}'.format(stock, hdf['close'][pre_entry_date],
                                                                               entry_price))
        print('=' * 80)
        print('done')

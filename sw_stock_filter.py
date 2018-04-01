#!/bin/python3

import sw_history
import sw_study

class StockFilter:

    def __init__(self, history = None, study = None):
        if history is None:
            history = sw_history.History()
        self._history = history
        if study is None:
            study = sw_study.Study(history)
        self._study = study

    def connors_filter(self, stock):
        '''
        Selects a stock if it is available for at least 200 days and
        it has min volume >= 250000 and min close >= 5 for last 21 days
        :param stock: stock e.g. 'AAPL'
        :return: True/False (selected or not)
        '''
        hdf = self._history.to_dataframe(stock)
        if hdf is None: return False
        if len(hdf) < 200: return False
        if min(hdf.iloc[-21:]['volume'].values) < 250000: return False
        if min(hdf.iloc[-21:]['close'].values) < 5: return False
        return True

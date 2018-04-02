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
        it is min volume >= 250000 and min close >= 5 for last 21 days
        :param stock: stock e.g. 'AAPL'
        :return: True/False (selected or not)
        '''
        hdf = self._history.to_dataframe(stock)
        if hdf is None: return False
        if len(hdf) < 200: return False
        if min(hdf.iloc[-21:]['volume'].values) < 250000: return False
        if min(hdf.iloc[-21:]['close'].values) < 5: return False
        return True

    def rocket_filter(self, stock):
        '''
        Selects a stock if it is 52-wk high or all-time high and
        it is ma-50 > ma_200 and close > ma-50 and
        volume > 4 * average volume for 60 days
        :param stock: stock e.g. 'AAPL'
        :return: True/False (selected or not)
        '''
        hdf = self._history.to_dataframe(stock)
        if hdf is None: return False
        if len(hdf) < 200: return False
        close = hdf.iloc[-1]['close']
        if close <= hdf.iloc[-250:-1]['close'].values.max(): return False
        ma_50 = hdf.iloc[-50:]['close'].values.mean()
        ma_200 = hdf.iloc[-200:]['close'].values.mean()
        if ma_50 <= ma_200: return False
        if close <= ma_50: return False
        volume = hdf.iloc[-1]['volume']
        if volume <= 4 * hdf.iloc[-60:-1]['volume'].values.mean(): return False
        return True

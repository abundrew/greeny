#!/bin/python3

import csv
import sw_config

class Stock:
    def __init__(self, path_stocks=sw_config.PATH_STOCKS, format_selected=sw_config.FORMAT_SELECTED):
        self._path_stocks = path_stocks
        self._format_selected = format_selected
        self._stocks = []
        self._stocks_nyse = []
        self._stocks_amex = []
        self._stocks_nasdaq = []
        with open(self._path_stocks, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                stock = row[0]
                if '.' in stock: continue
                if '-' in stock: continue
                self._stocks.append(stock)
                if row[7] == 'NYSE':
                    self._stocks_nyse.append(stock)
                elif row[7] == 'AMEX':
                    self._stocks_amex.append(stock)
                elif row[7] == 'NASDAQ':
                    self._stocks_nasdaq.append(stock)
        self._stocks.sort()
        self._stocks_nyse.sort()
        self._stocks_amex.sort()
        self._stocks_nasdaq.sort()

    def stocks(self, exchange='ALL'):
        if exchange == 'NYSE':
            return self._stocks_nyse[:]
        elif exchange == 'AMEX':
            return self._stocks_amex[:]
        elif exchange == 'NASDAQ':
            return self._stocks_nasdaq[:]
        else:
            return self._stocks[:]

    def selected(self, avail_days, check_days, check_volume, check_price=None, history=None):
        fname = self._format_selected.format('{}_{}_{}_{}'.format(avail_days, check_days, check_volume, check_price))
        if history is not None:
            selected = history.select(self.stocks(), avail_days, check_days, check_volume, check_price)
            with open(fname, 'w') as f:
                for s in selected:
                    f.write(s + '\n')
        with open(fname, 'r') as f:
            selected = [line.rstrip('\n') for line in f]
        return selected

    def trend_50_200(self, stocks, history, study):
        fname = self._format_selected.format('50_200')
        if history is not None and study is not None:
            selected = []
            for stock in stocks:
                hdf = history.to_dataframe(stock)
                sdf = study.to_dataframe(stock)
                if hdf is None: continue
                if sdf is None: continue
                #if not hdf.iloc[-1]['close'] > sdf.iloc[-1]['ma_50']: continue
                if not sdf.iloc[-1]['ma_50'] > sdf.iloc[-1]['ma_200']: continue
                selected.append(stock)
            with open(fname, 'w') as f:
                for s in selected:
                    f.write(s + '\n')
        with open(fname, 'r') as f:
            selected = [line.rstrip('\n') for line in f]
        return selected

# -------------------------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 60)
    print('test sw_stock.py...')
    print('-' * 60)
    try:
        s = Stock()
        for a in ('ALL', 'NYSE', 'AMEX', 'NASDAQ'):
            print('{:6} stocks: {} ...'.format(a, ' '.join(s.stocks(a)[:10])))
    except:
        import sys
        error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
        print(error)
    print('-' * 60)

#!/bin/python3

import os
import sys
import pandas as pd
import av_api
import sw_config

class History:
    def __init__(self, stock_a=sw_config.STOCK_A, format_history=sw_config.FORMAT_HISTORY):
        self._format_history = format_history
        self._stock_a = stock_a

    def to_dataframe(self, stock):
        try:
            fname = self._format_history.format(stock)
            if not os.path.isfile(fname): return None
            return pd.read_csv(fname, parse_dates=['date'], index_col='date')
        except:
            error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
            print(error)

    def to_series(self, stock, column):
        try:
            df = self.to_dataframe(stock)
            if df is None: return None
            return df[column]
        except:
            error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
            print(error)

    # outputsize: full
    def download(self, stocks, skip_if_exists=True):
        print('start downloading daily history...')
        if isinstance(stocks, str):
            stocks = [stocks]
        for stock in stocks:
            fname = self._format_history.format(stock)
            if skip_if_exists and os.path.isfile(fname):
                continue
            print(stock)
            try:
                data = av_api.time_series_daily_adjusted(stock, True)
                if (data['success']):
                    df = data['data']
                    df.to_csv(fname)
            except KeyboardInterrupt:
                error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
                print(error)
                break
            except:
                error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
                print(error)
        print('done downloading daily history !!!')

    # outputsize: compact
    def update(self, stocks):
        print('start updating history ...')
        data = av_api.time_series_daily_adjusted(self._stock_a)
        if not data['success']:
            print('ERROR - SYMBOL A')
            return
        update_date = str(data['data'].index.max())
        if isinstance(stocks, str):
            stocks = [stocks]
        for stock in stocks:
            fname = self._format_history.format(stock)
            print(stock)
            try:
                if not os.path.isfile(fname):
                    print('- file not found -')
                    continue
                df = pd.read_csv(fname, parse_dates=['date'], index_col='date')
                last_date = str(df.index.max())
                if last_date >= update_date:
                    print('+ up to date +')
                    continue
                data = av_api.time_series_daily_adjusted(stock)
                if not data['success']:
                    print('- api error -')
                    continue
                df_update = data['data']
                df_new = pd.concat([df, df_update[last_date:].iloc[1:]]).drop_duplicates()
                df_new.to_csv(fname)
            except KeyboardInterrupt:
                error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
                print(error)
                break
            except:
                error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
                print(error)
        print('done updating history !!!')

# -------------------------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 60)
    print('test sw_history.py...')
    print('-' * 60)
    try:
        h = History()
        data = h.to_dataframe('AAPL')
        print(data.tail())
    except:
        error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
        print(error)
    print('-' * 60)

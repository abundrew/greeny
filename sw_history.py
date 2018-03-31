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
        print('start downloading history...')
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
        print('done downloading history !!!')

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

    # avail_days - days at least available
    # check_days - days to check
    # check_volume - min volume to check
    # check_price - min close price to check
    def select(self, stocks, avail_days, check_days, check_volume, check_price=None):
        selected = []
        df = self.to_dataframe(self._stock_a)
        ix_avail_stock_a = list(df.index[-avail_days:])
        for stock in stocks:
            df = self.to_dataframe(stock)
            if df is None: continue
            if len(df) < avail_days: continue
            ix_avail = list(df.index[-avail_days:])
            if ix_avail != ix_avail_stock_a: continue
            if min(df.iloc[-check_days:]['volume'].values) < check_volume: continue
            if check_price is not None and min(df.iloc[-check_days:]['close'].values) < check_price: continue
            selected.append(stock)
        return selected

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

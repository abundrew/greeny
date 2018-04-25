#!/bin/python3

import os
import sys
import pandas as pd
import av
import config

class History:
    def __init__(self):
        self._reader = av.DataReader()

    def to_dataframe(self, symbol):
        try:
            fname = config.FORMAT_INTRADAY_HISTORY.format(symbol)
            if not os.path.isfile(fname): return None
            return pd.read_csv(fname, parse_dates=['date'], index_col='date')
        except:
            print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))

    # outputsize: full
    def download(self, symbols, skip_if_exists=True):
        print('-----> downloading intraday history ...')
        if isinstance(symbols, str):
            symbols = [symbols]
        for symbol in symbols:
            fname = config.FORMAT_INTRADAY_HISTORY.format(symbol)
            if skip_if_exists and os.path.isfile(fname):
                continue
            print(symbol)
            try:
                data = self._reader.time_series_intraday(symbol, '30min', True)
                if (data['success'] and data['data'] is not None):
                    df = data['data']
                    df.to_csv(fname)
            except KeyboardInterrupt:
                print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
                break
            except:
                print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        print('<----- downloading intraday history ...')

    # outputsize: compact
    def update(self, symbols):
        print('-----> updating intraday history ...')
        data = self._reader.time_series_intraday(config.SYMBOL_A, '30min')
        if not data['success']:
            print('ERROR: {}'.format(data['error']))
            return
        update_date = str(data['data'].index.max())
        if isinstance(symbols, str):
            symbols = [symbols]
        for symbol in symbols:
            fname = config.FORMAT_INTRADAY_HISTORY.format(symbol)
            print(symbol)
            try:
                if not os.path.isfile(fname):
                    print('- the file not found -')
                    continue
                df = pd.read_csv(fname, parse_dates=['date'], index_col='date')
                last_date = str(df.index.max())
                if last_date >= update_date:
                    print('+ data is up to date +')
                    continue
                data = self._reader.time_series_intraday(symbol, '30min')
                if not data['success']:
                    print('ERROR: {}'.format(data['error']))
                    continue
                if data['data'] is None:
                    continue
                df_update = data['data']
                df_new = pd.concat([df, df_update[last_date:].iloc[1:]]).drop_duplicates()
                df_new.to_csv(fname)
            except KeyboardInterrupt:
                print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
                break
            except:
                print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        print('<----- updating intraday history ...')

# ----- self-test -------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 80)
    print('test intraday.History ...')
    print('-' * 80)
    try:
        history = History()
        history.download('MSFT')
        data = history.to_dataframe('MSFT')
        print('MSFT ...')
        print(data.tail())
        history.update('MSFT')
        data = history.to_dataframe('MSFT')
        print('MSFT ...')
        print(data.tail())
    except:
        print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    print('-' * 80)

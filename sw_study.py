#!/bin/python3

import os
import sys
import pandas as pd
import sw_config
import sw_calc

class Study:
    def __init__(self, history, format_study=sw_config.FORMAT_STUDY):
        self._history = history
        self._format_study = format_study

    def to_dataframe(self, stock):
        try:
            fname = self._format_study.format(stock)
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

    # ---------------------------------------------------------------------------

    def RSI(self, series, n):
        return pd.Series(sw_calc.RSI(series.values, n), index=series.index)

    def updown_streak(self, series):
        return pd.Series(sw_calc.updown_streak(series.values), index=series.index)

    def RSI_streak(self, series, n):
        return pd.Series(sw_calc.RSI_streak(series.values, n), index=series.index)

    def percent_rank(self, series, n):
        return pd.Series(sw_calc.percent_rank(series.values, n), index=series.index)

    def Connors_RSI(self, series, n_rsi=3, n_streak=2, n_rank=100):
        return pd.Series(sw_calc.Connors_RSI(series.values, n_rsi, n_streak, n_rank), index=series.index)

    def ADX(self, hi_series, lo_series, cl_series, n):
        return pd.Series(sw_calc.ADX(hi_series.values, lo_series.values, cl_series.values, n), index=hi_series.index)

    # ---------------------------------------------------------------------------

    def update(self, stocks):
        print('start updating studies ...')
        if isinstance(stocks, str):
            stocks = [stocks]
        for stock in stocks:
            fname = self._format_study.format(stock)
            print(stock)
            try:
                df = self._history.to_dataframe(stock)
                if df is None: continue
                adx_10 = self.ADX(df['high'], df['low'], df['close'], 10).round(2)
                bb_mean = df['close'].rolling(20).mean().round(2)
                bb_std = df['close'].rolling(20).std().round(2)
                crsi = self.Connors_RSI(df['close'], 3, 2, 100).round(2)
                ma_200 = df['close'].rolling(200).mean().round(2)
                ma_50 = df['close'].rolling(50).mean().round(2)
                rsi_14 = self.RSI(df['close'], 14).round(2)
                df_study = pd.DataFrame(data={'adx_10': adx_10,
                                              'bb_mean': bb_mean,
                                              'bb_std': bb_std,
                                              'crsi': crsi,
                                              'ma_200': ma_200,
                                              'ma_50': ma_50,
                                              'rsi_14': rsi_14}, index=df.index)
                df_study.to_csv(fname)
            except KeyboardInterrupt:
                error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
                print(error)
                break
            except:
                error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
                print(error)
        print('done updating studies !!!')

# -------------------------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 60)
    print('test sw_study.py...')
    print('-' * 60)
    try:
        import sw_history
        h = sw_history.History()
        s = Study(h)
        data = s.to_dataframe('AAPL')
        print(data.tail())
    except:
        error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
        print(error)
    print('-' * 60)

#!/bin/python3

import pandas as pd
import sw_calc

class Exit:
    def __init__(self, n_rsi, v_rsi, n_limit):
        self.n_rsi = n_rsi
        self.v_rsi = v_rsi
        self.n_limit = n_limit

    def description(self):
        return "{}-day RSI 'close' above {}, limit {} days".format(self.n_rs, self.v_rs, self.n_limit)

    def exit(self, history_df, study_df, pre_entry_date):
        hdf = history_df

        if not pre_entry_date in hdf.index: return None
        pre_entry_date_loc = hdf.index.get_loc(pre_entry_date)
        if pre_entry_date_loc == len(hdf.index) - 1: return None
        entry_date_loc = pre_entry_date_loc + 1
        rsi = pd.Series(sw_calc.RSI(hdf['close'].values, self.n_rsi), index=hdf['close'].index)
        dates = hdf.index[entry_date_loc + 1:entry_date_loc + self.n_limit + 1]
        if len(dates) == 0: return None
        exit_price = hdf['open'][dates[-1]]
        for i in range(1, len(dates) - 1):
            if rsi[dates[-i - 1]] > self.v_rsi:
                exit_price = hdf['open'][dates[-i]]
        return exit_price

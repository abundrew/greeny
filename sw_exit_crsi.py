#!/bin/python3

class Exit:
    def __init__(self, v_crsi, n_limit):
        self.v_crsi = v_crsi
        self.n_limit = n_limit

    def description(self):
        return "CRSI 'close' above {}, limit {} days".format(self.v_crsi, self.n_limit)

    def exit(self, history_df, study_df, pre_entry_date):
        hdf = history_df
        sdf = study_df

        if not pre_entry_date in hdf.index: return None
        pre_entry_date_loc = hdf.index.get_loc(pre_entry_date)
        if pre_entry_date_loc == len(hdf.index) - 1: return None
        entry_date_loc = pre_entry_date_loc + 1
        dates = hdf.index[entry_date_loc + 1:entry_date_loc + self.n_limit + 1]
        if len(dates) == 0: return None
        exit_price = hdf['open'][dates[-1]]
        for i in range(1, len(dates) - 1):
            if sdf['crsi'][dates[-i - 1]] > self.v_crsi:
                exit_price = hdf['open'][dates[-i]]
        return exit_price

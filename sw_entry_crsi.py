#!/bin/python3

class Entry:

    # W - sell off : low < (100 - W(%)) * prev.close : 2,4,6,8
    # X - closing range : close - low < (high - low) * X(%) : 10,25
    # Y - entry CRSI : 5,6,7,...,15
    # Z - entry limit : 4,6,8,10

    # N = [50,70,80,80,80,80]
    # W = [ 2, 4, 8, 2, 6, 8]
    # X = [25,25,25,10,10,10]
    # Y = [ 8, 6, 8, 5, 8,10]
    # Z = [10,10,10,10,10,10]

    def __init__(self, W, X, Y, Z):
        self.W = W
        self.X = X
        self.Y = Y
        self.Z = Z
        pass

    def entry(self, history_df, study_df, pre_entry_date, test=False):
        hdf = history_df
        sdf = study_df

        if hdf is None or not pre_entry_date in hdf.index: return None
        if sdf is None or not pre_entry_date in sdf.index: return None

        hrdate0 = hdf.loc[pre_entry_date]
        srdate0 = sdf.loc[pre_entry_date]

        pre_entry_date_loc = hdf.index.get_loc(pre_entry_date)
        if pre_entry_date_loc == 0: return 0
        hrdate1 = hdf.iloc[pre_entry_date_loc - 1]

        if not srdate0['adx_10'] > 30: return None
        if not hrdate0['low'] <= (100. - self.W) * hrdate1['close'] / 100: return None
        if not hrdate0['close'] <= hrdate0['low'] + (100. - self.X) * (
                hrdate0['high'] - hrdate0['low']) / 100: return None
        if not srdate0['crsi'] < self.Y: return None

        entry_price = (100. - self.Z) * hrdate0['close'] / 100

        if test:
            pre_entry_date_loc = hdf.index.get_loc(pre_entry_date)
            if pre_entry_date_loc == len(hdf.index) - 1: return None
            entry_date = str(hdf.index[pre_entry_date_loc + 1])
            if hdf['low'][entry_date] > entry_price: return None

        return entry_price

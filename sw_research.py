#!/bin/python3

import pandas as pd

class Research:
    def __init__(self, history, study):
        self._history = history
        self._study = study

    def trade(self, history_df, study_df, pre_entry_date, entry_func, exit_func):
        hdf = history_df
        sdf = study_df

        entry_price = entry_func(hdf, sdf, pre_entry_date, True)
        if entry_price is not None and entry_price > 0:
            exit_price = exit_func(hdf, sdf, pre_entry_date)
            if exit_price is not None:
                return (exit_price - entry_price) / entry_price
        return None

    def test(self, stocks, start_date, end_date, entry_func, exit_func, silent=False, filename=None, description=''):
        total_trades = 0
        total_gain = 0
        total_wins = 0
        if isinstance(stocks, str):
            stocks = [stocks]

        s = '{0}\n{1}\n       Trades   Gain%   Wins% +Trades  +Gain%  +Wins%\n{1}\n'.format(description, '-' * 53)
        if not silent:
            print(s, end='')
        if not filename is None:
            with open(filename, 'a') as f:
                f.write(s)

        for stock in stocks:
            n_trades = 0
            m_gain = 0
            n_wins = 0
            hdf = self._history.to_dataframe(stock)
            sdf = self._study.to_dataframe(stock)
            for pre_entry_date in pd.date_range(start_date, end_date):
                gain = self.trade(hdf, sdf, pre_entry_date, entry_func, exit_func)
                if gain is None:
                    continue
                n_trades += 1
                m_gain += gain
                if gain > 0:
                    n_wins += 1
            total_trades += n_trades
            total_gain += m_gain
            total_wins += n_wins

            if n_trades > 0:
                s = '{:5}  {:6}  {:6.2f}  {:6.2f}  {:6}  {:6.2f}  {:6.2f}\n'.format(
                    stock,
                    n_trades,
                    100. * m_gain / n_trades if n_trades > 0 else 0,
                    100. * n_wins / n_trades if n_trades > 0 else 0,
                    total_trades,
                    100. * total_gain / total_trades if total_trades > 0 else 0,
                    100. * total_wins / total_trades if total_trades > 0 else 0)
                if not silent:
                    print(s, end='')
                if not filename is None:
                    with open(filename, 'a') as f:
                        f.write(s)

        s = '{}\n{} ... {:14} {:7}  {:6.2f}  {:6.2f}\n'.format(
            '-' * 53,
            start_date,
            end_date,
            total_trades,
            100. * total_gain / total_trades if total_trades > 0 else 0,
            100. * total_wins / total_trades if total_trades > 0 else 0)
        if not silent:
            print(s, end='')
        if not filename is None:
            with open(filename, 'a') as f:
                f.write(s)

        return {'trades': total_trades, 'gain': total_gain, 'wins': total_wins}

    # freq = Y, Q, M
    def super_test(self, stocks, start_date, end_date, freq, entry_func, exit_func, filename=None):
        total_trades = 0
        total_gain = 0
        total_wins = 0
        if isinstance(stocks, str):
            stocks = [stocks]

        s = '{0}\n{1}Trades   Gain%   Wins% +Trades  +Gain%  +Wins%\n{0}\n'.format('-' * 70, ' ' * 24)
        print(s, end='')
        if not filename is None:
            with open(filename, 'a') as f:
                f.write(s)

        freq_start, freq_end = 'AS', 'A'
        if freq == 'Q':
            freq_start, freq_end = 'QS', 'Q'
        if freq == 'M':
            freq_start, freq_end = 'MS', 'M'
        ranges = zip(
            map(str, pd.date_range(start_date, end_date, None, freq_start)),
            map(str, pd.date_range(start_date, end_date, None, freq_end)))

        for s_date, e_date in ranges:
            data = self.test(stocks, s_date, e_date, entry_func, exit_func, True, None, '')
            n_trades = data['trades']
            m_gain = data['gain']
            n_wins = data['wins']
            total_trades += n_trades
            total_gain += m_gain
            total_wins += n_wins

            if n_trades > 0:
                s = '{}..{}  {:6}  {:6.2f}  {:6.2f}  {:6}  {:6.2f}  {:6.2f}\n'.format(
                    s_date[:10],
                    e_date[:10],
                    n_trades,
                    100. * m_gain / n_trades if n_trades > 0 else 0,
                    100. * n_wins / n_trades if n_trades > 0 else 0,
                    total_trades,
                    100. * total_gain / total_trades if total_trades > 0 else 0,
                    100. * total_wins / total_trades if total_trades > 0 else 0)
                print(s, end='')
                if not filename is None:
                    with open(filename, 'a') as f:
                        f.write(s)

        s = '{}\n{}..{:34} {:7}  {:6.2f}  {:6.2f}\n'.format(
            '-' * 70,
            start_date,
            end_date,
            total_trades,
            100. * total_gain / total_trades if total_trades > 0 else 0,
            100. * total_wins / total_trades if total_trades > 0 else 0)
        print(s, end='')
        if not filename is None:
            with open(filename, 'a') as f:
                f.write(s)

        return {'trades': total_trades, 'gain': total_gain, 'wins': total_wins}

# -------------------------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 60)
    print('test sw_research.py...')
    print('-' * 60)
    try:
        import sw_history
        import sw_study
        h = sw_history.History()
        s = sw_study.Study(h)
        r = Research(h, s)

        def entry(history_df, study_df, pre_entry_date, test=False):
            hdf = history_df
            sdf = study_df

            if not pre_entry_date in hdf.index: return None
            if not pre_entry_date in sdf.index: return None
            if not hdf['close'][pre_entry_date] > sdf['ma_50'][pre_entry_date]: return None
            if not sdf['ma_50'][pre_entry_date] > sdf['ma_200'][pre_entry_date]: return None

            pre_entry_date_loc = hdf.index.get_loc(pre_entry_date)
            if pre_entry_date_loc >= len(hdf.index) - 1: return None
            entry_date = str(hdf.index[pre_entry_date_loc + 1])
            entry_price = hdf['open'][entry_date]
            return entry_price

        def exit(history_df, study_df, pre_entry_date):
            hdf = history_df

            if not pre_entry_date in hdf.index: return None
            pre_entry_date_loc = hdf.index.get_loc(pre_entry_date)
            if pre_entry_date_loc >= len(hdf.index) - 5: return None
            exit_date = str(hdf.index[pre_entry_date_loc + 5])
            exit_price = hdf['close'][exit_date]
            return exit_price

        r.super_test('AAPL', '2000-01-01', '2018-12-31', 'Q', entry, exit)
    except:
        import sys
        error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
        print(error)
    print('-' * 60)

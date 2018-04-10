#!/bin/python3

import pandas as pd
import sys
import stock

class Strategy:
    def __init__(self, stocks, entry=None, exit=None):
        self._stocks = stocks
        self._entry = entry if entry is not None else self._default_entry
        self._exit = exit if exit is not None else self._default_exit

    def set_entry(self, entry=None):
        self._entry = entry if entry is not None else self._default_entry

    def set_exit(self, exit=None):
        self._exit = exit if exit is not None else self._default_exit

    def _default_entry(self, stock, pre_entry_date):
        hdf = stock.history()
        if hdf is None or not pre_entry_date in hdf.index: return None
        return hdf['close'][pre_entry_date]

    def _default_exit(self, stock, post_entry_date):
        hdf = stock.history()
        if hdf is None or not post_entry_date in hdf.index: return None
        return hdf['close'][post_entry_date]

    def trade(self, stock, pre_entry_date):
        hdf = stock.history()
        entry_price = self._entry(stock, pre_entry_date)
        if entry_price is not None and entry_price > 0:
            pre_entry_date_loc = hdf.index.get_loc(pre_entry_date)
            if pre_entry_date_loc + 3 > len(hdf.index): return None
            exit_price = self._exit(stock, str(hdf.index[pre_entry_date_loc + 2]))
            if exit_price is not None:
                return (exit_price - entry_price) / entry_price
        return None

    def test(self, start_date, end_date, silent=False):
        total_trades = 0
        total_gain = 0
        total_wins = 0
        if not silent:
            s = '{0}\n       Trades   Gain%   Wins%  +Trades  +Gain%  +Wins%\n{0}\n'.format('-' * 54)
            print(s, end='')

        for symbol in self._stocks:
            n_trades = 0
            m_gain = 0
            n_wins = 0
            for pre_entry_date in pd.date_range(start_date, end_date):
                gain = self.trade(self._stocks[symbol], pre_entry_date)
                if gain is None: continue
                n_trades += 1
                m_gain += gain
                if gain > 0: n_wins += 1
            total_trades += n_trades
            total_gain += m_gain
            total_wins += n_wins

            if not silent and n_trades > 0:
                s = '{:5}  {:6}  {:6.2f}  {:6.2f}   {:6}  {:6.2f}  {:6.2f}\n'.format(
                    symbol,
                    n_trades,
                    100. * m_gain / n_trades if n_trades > 0 else 0,
                    100. * n_wins / n_trades if n_trades > 0 else 0,
                    total_trades,
                    100. * total_gain / total_trades if total_trades > 0 else 0,
                    100. * total_wins / total_trades if total_trades > 0 else 0)
                print(s, end='')

        if not silent:
            s = '{}\n{} ... {:14}  {:7}  {:6.2f}  {:6.2f}\n'.format(
                '-' * 54,
                start_date,
                end_date,
                total_trades,
                100. * total_gain / total_trades if total_trades > 0 else 0,
                100. * total_wins / total_trades if total_trades > 0 else 0)
            print(s, end='')

        return {'trades': total_trades, 'gain': total_gain, 'wins': total_wins}

    # freq = Y, Q, M
    def test_plus(self, start_date, end_date, freq):
        total_trades = 0
        total_gain = 0
        total_wins = 0

        s = '{0}\n{1}Trades   Gain%   Wins%  +Trades  +Gain%  +Wins%\n{0}\n'.format('-' * 71, ' ' * 24)
        print(s, end='')

        freq_start, freq_end = 'AS', 'A'
        if freq == 'Q':
            freq_start, freq_end = 'QS', 'Q'
        if freq == 'M':
            freq_start, freq_end = 'MS', 'M'
        ranges = zip(
            map(str, pd.date_range(start_date, end_date, None, freq_start)),
            map(str, pd.date_range(start_date, end_date, None, freq_end)))

        for s_date, e_date in ranges:
            data = self.test(s_date, e_date, True)
            n_trades = data['trades']
            m_gain = data['gain']
            n_wins = data['wins']
            total_trades += n_trades
            total_gain += m_gain
            total_wins += n_wins

            if n_trades > 0:
                s = '{}..{}  {:6}  {:6.2f}  {:6.2f}   {:6}  {:6.2f}  {:6.2f}\n'.format(
                    s_date[:10],
                    e_date[:10],
                    n_trades,
                    100. * m_gain / n_trades if n_trades > 0 else 0,
                    100. * n_wins / n_trades if n_trades > 0 else 0,
                    total_trades,
                    100. * total_gain / total_trades if total_trades > 0 else 0,
                    100. * total_wins / total_trades if total_trades > 0 else 0)
                print(s, end='')

        s = '{}\n{}..{:34}  {:7}  {:6.2f}  {:6.2f}\n'.format(
            '-' * 71,
            start_date,
            end_date,
            total_trades,
            100. * total_gain / total_trades if total_trades > 0 else 0,
            100. * total_wins / total_trades if total_trades > 0 else 0)
        print(s, end='')

        return {'trades': total_trades, 'gain': total_gain, 'wins': total_wins}

    def setup(self, pre_entry_date):
        pass

# ----- self-test -------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 80)
    print('test strategy.Strategy ...')
    print('-' * 80)
    try:
        strategy = Strategy(stock.stocks(['AAPL','MSFT']))
        #strategy = Strategy(stock.Selection().select(['UPTREND','MORE_20','LIQUID','CRSI_20']))
        strategy.test('2000-01-01', '2019-01-01')
        strategy.test_plus('2000-01-01', '2019-01-01', 'Y')
    except:
        print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    print('-' * 80)

#!/bin/python3

import pandas as pd
import stock

class Strategy:
    def __init__(self, symbols, entry=None, exit=None):
        self._stocks = {}
        for symbol in symbols:
            self._stocks[symbol] = stock.Stock(symbol)
        self._entry = entry if entry is not None else self._dummy_entry
        self._exit = exit if exit is not None else self._dummy_exit

    def set_entry(self, entry=None):
        self._entry = entry if entry is not None else self._dummy_entry

    def set_exit(self, exit=None):
        self._exit = exit if exit is not None else self._dummy_exit

    def _dummy_entry(self, stock, pre_entry_date):
        return None

    def _dummy_exit(self, stock, post_entry_date):
        return None

    def trade(self, stock, pre_entry_date):
        entry_price = self._entry(stock, pre_entry_date)
        if entry_price is not None and entry_price > 0:
            exit_price = self._exit(stock, pre_entry_date + 2)
            if exit_price is not None:
                return (exit_price - entry_price) / entry_price
        return None

    def test(self, symbols, start_date, end_date):
        if isinstance(symbols, str):
            symbols = [symbols]
        for pre_entry_date in pd.date_range(start_date, end_date):
            pass

    def setup(self, pre_entry_date):
        pass

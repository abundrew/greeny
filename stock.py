#!/bin/python3

import csv
import os
import sys
import config

class Symbol:
    def __init__(self):
        self._symbols = []
        self._symbols_nyse = []
        self._symbols_amex = []
        self._symbols_nasdaq = []
        with open(config.PATH_SYMBOLS, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                symbol = row[0]
                if '.' in symbol: continue
                if '-' in symbol: continue
                self._symbols.append(symbol)
                if row[7] == 'NYSE':
                    self._symbols_nyse.append(symbol)
                elif row[7] == 'AMEX':
                    self._symbols_amex.append(symbol)
                elif row[7] == 'NASDAQ':
                    self._symbols_nasdaq.append(symbol)
        self._symbols.sort()
        self._symbols_nyse.sort()
        self._symbols_amex.sort()
        self._symbols_nasdaq.sort()

    def symbols(self, selection='ALL'):
        if selection == 'ALL':
            return self._symbols[:]
        elif selection == 'NYSE':
            return self._symbols_nyse[:]
        elif selection == 'AMEX':
            return self._symbols_amex[:]
        elif selection == 'NASDAQ':
            return self._symbols_nasdaq[:]
        else:
            fname = config.FORMAT_SYMBOLS.format(selection)
            if not os.path.isfile(fname): return None
            with open(fname, 'r') as f:
                selected = [line.rstrip('\n') for line in f]
            return selected

    def save_selection(self, selection, symbols):
        fname = config.FORMAT_SYMBOLS.format(selection)
        with open(fname, 'w') as f:
            for symbol in symbols:
                f.write(symbol + '\n')

# ----- self-test -------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 80)
    print('test stock.Symbol ...')
    print('-' * 80)
    try:
        symbol = Symbol()
        for selection in ['ALL', 'NYSE', 'AMEX', 'NASDAQ']:
            print('{} : {}'.format(selection.ljust(9), len(symbol.symbols(selection))))
        symbol.save_selection('AAPL_MSFT', ['AAPL', 'MSFT'])
        print('{} : {}'.format('AAPL_MSFT', symbol.symbols('AAPL_MSFT')))
    except:
        print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    print('-' * 80)

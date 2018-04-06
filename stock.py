#!/bin/python3

import csv
import json
import os
import sys
import config
import iex
import daily

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

class Fundamentals:
    def __init__(self):
        if not os.path.isfile(config.PATH_FINANCIALS):
            self.update()
        with open(config.PATH_FINANCIALS) as f:
            self._financials = json.load(f)
        if not os.path.isfile(config.PATH_PEERS):
            self.update()
        with open(config.PATH_PEERS) as f:
            self._peers = json.load(f)
        if not os.path.isfile(config.PATH_STATS):
            self.update()
        with open(config.PATH_STATS) as f:
            self._stats = json.load(f)

    def financials(self, symbol):
        try:
            return self._financials['data'][symbol]['financials']['financials']
        except:
            print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))

    def peers(self, symbol):
        try:
            return self._peers['data'][symbol]['peers']
        except:
            print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))

    def stats(self, symbol):
        try:
            return self._stats['data'][symbol]['stats']
        except:
            print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))

    def update(self):
        reader = iex.DataReader()
        symbols = Symbol().symbols()
        component = {'financials':config.PATH_FINANCIALS,
                     'peers':config.PATH_PEERS,
                     'stats':config.PATH_STATS}
        for key in component:
            fname = component[key]
            bname = fname + '.bak'
            if os.path.isfile(fname):
                if os.path.isfile(bname):
                    os.remove(bname)
                os.rename(fname, fname + '.bak')
            data = reader.stock_batch_100(symbols, key)
            s = json.dumps(data)
            with open(fname, 'w') as f:
                f.write(s)

class Stock:
    def __init__(self, symbol):
        history = daily.History()
        study = daily.Study()
        fundamentals = Fundamentals()
        self._symbol = symbol
        self._history = history.to_dataframe(symbol)
        self._study = study.to_dataframe(symbol)
        self._financials = fundamentals.financials(symbol)
        self._peers = fundamentals.peers(symbol)
        self._stats = fundamentals.stats(symbol)

    def symbol(self):
        return self._symbol

    def history(self):
        return self._history

    def study(self):
        return self._study

    def financials(self):
        return self._financials

    def peers(self):
        return self._peers

    def stats(self):
        return self._stats

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
    print('test stock.Fundamentals ...')
    print('-' * 80)
    try:
        fundamentals = Fundamentals()
        #fundamentals.update()
        print('Financials MSFT')
        financials = fundamentals.financials('MSFT')
        for key in list(financials[0])[:3]:
            print('{} : {}'.format(key, financials[0][key]))
        print('...')
        print('Peers MSFT ...')
        print(fundamentals.peers('MSFT'))
        print('Stats MSFT ...')
        stats = fundamentals.stats('MSFT')
        for key in list(stats)[:3]:
            print('{} : {}'.format(key, stats[key]))
        print('...')
    except:
        print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    print('-' * 80)
    print('test stock.Stock ...')
    print('-' * 80)
    try:
        stock = Stock('MSFT')
        print('Daily History {}'.format(stock.symbol()))
        print(stock.history().tail())
        print('Daily Study {}'.format(stock.symbol()))
        print(stock.study().tail())
        print('Financials {}'.format(stock.symbol()))
        financials = stock.financials()
        for key in list(financials[0])[:3]:
            print('{} : {}'.format(key, financials[0][key]))
        print('...')
        print('Peers {}'.format(stock.symbol()))
        peers = stock.peers()
        print(peers)
        print('Stats {}'.format(stock.symbol()))
        stats = stock.stats()
        for key in list(stats)[:3]:
            print('{} : {}'.format(key, stats[key]))
        print('...')
    except:
        print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    print('-' * 80)

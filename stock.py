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
        with open(config.PATH_SYMBOLS, 'r') as f:
            for symbol in f.read().splitlines():
                if '.' in symbol: continue
                if '-' in symbol: continue
                self._symbols.append(symbol)
        self._symbols.sort()

    def symbols(self, selection='ALL'):
        if selection == 'ALL':
            return self._symbols[:]
        else:
            return Selection().select(selection)

class Selection:
    def __init__(self):
        pass

    def select(self, selections):
        if isinstance(selections, str):
            selections = [selections]
        interselected = Symbol().symbols()
        for selection in selections:
            fname = config.FORMAT_SYMBOLS.format(selection)
            if not os.path.isfile(fname): continue
            with open(fname, 'r') as f:
                selected = [line.rstrip('\n') for line in f]
            interselected = list(set(interselected) & set(selected))
        interselected.sort()
        return interselected

    def save(self, selection, symbols):
        fname = config.FORMAT_SYMBOLS.format(selection)
        with open(fname, 'w') as f:
            for symbol in symbols:
                f.write(symbol + '\n')

    def update(self):
        print('-----> updating selection ...')
        symbols = Symbol().symbols()
        history = daily.History()
        study = daily.Study()
        fundamentals = Fundamentals()

        selected_UPTREND = []
        selected_ROCKET = []
        selected_CONNORS = []
        selected_MORE_5 = []
        selected_MORE_20 = []
        selected_LESS_100 = []
        selected_LIQUID = []
        selected_CRSI_5 = []
        selected_CRSI_10 = []
        selected_CRSI_20 = []
        selected_CRSI_25 = []
        selected_OVERSOLD = []
        selected_OVERBOUGHT = []

        for symbol in symbols:
            hdf = history.to_dataframe(symbol)
            sdf = study.to_dataframe(symbol)
            stats = fundamentals.stats(symbol)
            if hdf is None: continue
            if sdf is None: continue
            if stats is None: continue

            # UPTREND
            # close > ma-50
            # ma-50 > ma_200
            if (
                    hdf.iloc[-1]['close'] > sdf.iloc[-1]['ma_50'] and
                    sdf.iloc[-1]['ma_50'] > sdf.iloc[-1]['ma_200']
            ): selected_UPTREND.append(symbol)

            # ROCKET
            # 52-wk high or all-time high
            # ma-50 > ma_200
            # close > ma-50
            # volume > 4 * average volume for 60 days
            if (
                    len(hdf) > 200 and
                    hdf.iloc[-1]['close'] > hdf.iloc[-250:-1]['close'].values.max() and
                    sdf.iloc[-1]['ma_50'] > sdf.iloc[-1]['ma_200'] and
                    hdf.iloc[-1]['close'] > sdf.iloc[-1]['ma_50'] and
                    hdf.iloc[-1]['volume'] > 4 * hdf.iloc[-60:-1]['volume'].values.mean()
            ): selected_ROCKET.append(symbol)

            # CONNORS
            # available > 200 days
            # min volume >= 250K for 21 days
            # min close >= 5 for 21 days
            if (
                    len(hdf) > 200 and
                    min(hdf.iloc[-21:]['volume'].values) > 250000 and
                    min(hdf.iloc[-21:]['close'].values) > 5
            ): selected_CONNORS.append(symbol)

            # MORE_5
            # close > 5
            if (
                    hdf.iloc[-1]['close'] > 5
            ): selected_MORE_5.append(symbol)

            # MORE_20
            # close > 20
            if (
                    hdf.iloc[-1]['close'] > 20
            ): selected_MORE_20.append(symbol)

            # LESS_100
            # close < 100
            if (
                    hdf.iloc[-1]['close'] < 100
            ): selected_LESS_100.append(symbol)

            # LIQUID
            # average volume > 500K for 50 days
            # market cap > 1B
            if (
                    len(hdf) > 50 and
                    hdf.iloc[-50:-1]['volume'].values.mean() > 500000 and
                    int(stats['marketcap']) > 1000000000
            ): selected_LIQUID.append(symbol)

            # CRSI_5
            # crsi < 5
            if (
                    sdf.iloc[-1]['crsi'] < 5
            ): selected_CRSI_5.append(symbol)

            # CRSI_10
            # crsi < 10
            if (
                    sdf.iloc[-1]['crsi'] < 10
            ): selected_CRSI_10.append(symbol)

            # CRSI_20
            # crsi < 20
            if (
                    sdf.iloc[-1]['crsi'] < 20
            ): selected_CRSI_20.append(symbol)

            # CRSI_25
            # crsi < 25
            if (
                    sdf.iloc[-1]['crsi'] < 25
            ): selected_CRSI_25.append(symbol)

            # OVERSOLD
            # rsi_14 < 30
            if (
                    sdf.iloc[-1]['rsi_14'] < 30
            ): selected_OVERSOLD.append(symbol)

            # OVERBOUGHT
            # rsi_14 > 70
            if (
                    sdf.iloc[-1]['rsi_14'] > 70
            ): selected_OVERBOUGHT.append(symbol)

        self.save('UPTREND', selected_UPTREND)
        self.save('ROCKET', selected_ROCKET)
        self.save('CONNORS', selected_CONNORS)
        self.save('MORE_5', selected_MORE_5)
        self.save('MORE_20', selected_MORE_20)
        self.save('LESS_100', selected_LESS_100)
        self.save('LIQUID', selected_LIQUID)
        self.save('CRSI_5', selected_CRSI_5)
        self.save('CRSI_10', selected_CRSI_10)
        self.save('CRSI_20', selected_CRSI_20)
        self.save('CRSI_25', selected_CRSI_25)
        self.save('OVERSOLD', selected_OVERSOLD)
        self.save('OVERBOUGHT', selected_OVERBOUGHT)
        print('<----- updating selection ...')

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
        print('-----> updating fundamentals ...')
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
            print(key)
        print('<----- updating fundamentals ...')

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

def stocks(symbols):
    stocks = {}
    for symbol in symbols:
        stocks[symbol] = Stock(symbol)
    return stocks

# ----- self-test -------------------------------------------------------------

if __name__ == "__main__":
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
    print('test stock.Symbol ...')
    print('-' * 80)
    try:
        symbol = Symbol()
        for selection in ['ALL', 'NYSE', 'AMEX', 'NASDAQ']:
            print('{} : {}'.format(selection.ljust(9), len(symbol.symbols(selection))))
    except:
        print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    print('-' * 80)
    print('test stock.Selection ...')
    print('-' * 80)
    try:
        selection = Selection()
        selection.update()
        for key in ['UPTREND','ROCKET','CONNORS','MORE_5','MORE_20','LESS_100','LIQUID','CRSI_5','CRSI_10', 'OVERSOLD', 'OVERBOUGHT']:
            selected = selection.select(key)
            print('{}: {} {} ...'.format(key.ljust(40), len(selected), ' '.join(selected[:10])))
        selected = selection.select(['UPTREND','MORE_20','LIQUID'])
        print('{}: {} {} ...'.format('UPTREND & MORE_20 & LIQUID'.ljust(40), len(selected), ' '.join(selected[:10])))
        selected = selection.select(['UPTREND','MORE_20','LIQUID','CRSI_20'])
        print('{}: {} {} ...'.format('UPTREND & MORE_20 & LIQUID & CRSI_20'.ljust(40), len(selected), ' '.join(selected[:10])))
        selected = selection.select(['UPTREND','MORE_20','LIQUID','OVERSOLD'])
        print('{}: {} {} ...'.format('UPTREND & MORE_20 & LIQUID & OVERSOLD'.ljust(40), len(selected), ' '.join(selected[:10])))
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

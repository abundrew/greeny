#!/bin/python3

import json
import urllib.request

class DataReader:
    def __init__(self):
        pass

    def _stock_api(self, endpoint):
        result = {}
        try:
            url = 'https://api.iextrading.com/1.0/' + endpoint
            headers = {}
            headers['User-Agent'] = ("Mozilla/5.0 (X11; Linux i686) "
                                     "AppleWebKit/537.17 (KHTML, like Gecko) "
                                     "Chrome/24.0.1312.27 Safari/537.17")
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            data = resp.read()
            encoding = resp.info().get_content_charset('utf-8')
            data = json.loads(data.decode(encoding))
            result['data'] = data
            result['success'] = True
            result['error'] = None
        except Exception as e:
            result['data'] = None
            result['success'] = False
            result['error'] = str(e)
        return result

    def stock_symbols(self):
        endpoint = "ref-data/symbols"
        data = self._stock_api(endpoint)
        if data['success']:
            data['data'] = [x for x in data['data'] if x['type'] in ['cs', 'et'] and x['isEnabled']]
        return data

    def _stock_batch(self, symbols, types='ohlc', range='1m'):
        endpoint = "stock/market/batch?symbols={}&types={}&range={}".format(','.join(symbols), types, range)
        data = self._stock_api(endpoint)
        return data

    def _stock_batch_100(self, symbols, types='ohlc', range='1m'):
        result = {}
        result['data'] = {}
        lst_sym = []
        for sym in symbols:
            lst_sym.append(sym)
            if len(lst_sym) == 100:
                batch_100 = self._stock_batch(lst_sym, types, range)
                if batch_100['success']:
                    for k, v in batch_100['data'].items():
                        result['data'][k] = v
                lst_sym[:] = []
        if len(lst_sym) > 0:
            batch_100 = self._stock_batch(lst_sym, types, range)
            if batch_100['success']:
                for k, v in batch_100['data'].items():
                    result['data'][k] = v
        result['success'] = True
        result['error'] = None
        return result

    def stock_book(self, symbol):
        endpoint = "stock/{}/book".format(symbol)
        data = self._stock_api(endpoint)
        return data

    def stock_chart(self, symbol, range='1m'):
        endpoint = "stock/{}/chart/{}".format(symbol, range)
        data = self._stock_api(endpoint)
        return data

    def stock_company(self, symbol):
        endpoint = "stock/{}/company".format(symbol)
        data = self._stock_api(endpoint)
        return data

    def stock_delayed_quote(self, symbol):
        endpoint = "stock/{}/delayed-quote".format(symbol)
        data = self._stock_api(endpoint)
        return data

    def stock_earnings(self, symbol):
        endpoint = "stock/{}/earnings".format(symbol)
        data = self._stock_api(endpoint)
        return data

    def stock_effective_spread(self, symbol):
        endpoint = "stock/{}/effective-spread".format(symbol)
        data = self._stock_api(endpoint)
        return data

    def stock_dividends(self, symbol, range='1m'):
        endpoint = "stock/{}/dividends/{}".format(symbol, range)
        data = self._stock_api(endpoint)
        return data

    def stock_financials(self, symbol):
        endpoint = "stock/{}/financials".format(symbol)
        data = self._stock_api(endpoint)
        return data

    def stock_stats(self, symbol):
        endpoint = "stock/{}/stats".format(symbol)
        data = self._stock_api(endpoint)
        return data

    def stock_ohlc(self, symbol=None):
        endpoint = "stock/{}/ohlc".format(('market' if symbol is None else symbol))
        data = self._stock_api(endpoint)
        for key in (str(key) for key in range(4)):
            if key in data['data']:
                del data['data'][key]
        return data

    def stock_peers(self, symbol):
        endpoint = "stock/{}/peers".format(symbol)
        data = self._stock_api(endpoint)
        return data

    def stock_previous(self, symbol=None):
        endpoint = "stock/{}/previous".format(('market' if symbol is None else symbol))
        data = self._stock_api(endpoint)
        return data

    def stock_price(self, symbol):
        endpoint = "stock/{}/price".format(symbol)
        data = self._stock_api(endpoint)
        return data

    def stock_quote(self, symbol, displayPercent=False):
        endpoint = "stock/{}/quote{}".format(symbol, ('?displayPercent=true' if displayPercent else ''))
        data = self._stock_api(endpoint)
        return data

    def stock_relevant(self, symbol):
        endpoint = "stock/{}/relevant".format(symbol)
        data = self._stock_api(endpoint)
        return data

    def stock_splits(self, symbol, range='1m'):
        endpoint = "stock/{}/splits/{}".format(symbol, range)
        data = self._stock_api(endpoint)
        return data

    def stock_volume_by_venue(self, symbol):
        endpoint = "stock/{}/volume-by-venue".format(symbol)
        data = self._stock_api(endpoint)
        return data

# ----- self-test -------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 80)
    print('test iex.DataReader ...')
    print('-' * 80)
    try:
        reader = DataReader()
        data = reader.stock_stats('AAPL')
        if data['success']:
            print('STATS AAPL')
            for key in data['data']:
                print('{} : {}'.format(key, data['data'][key]))
        else:
            print('ERROR: {}'.format(data['error']))
    except:
        import sys
        error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
        print(error)
    print('-' * 80)

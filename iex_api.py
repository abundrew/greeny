import json
import urllib.request

def stock_api(endpoint):
    result = {}
    try:
        url = 'https://api.iextrading.com/1.0/' + endpoint
        headers = {}
        headers[
            'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
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

bad_symbols = ['ATAX', 'BIL', 'CLGN', 'SHV', 'TMSR']

def stock_symbols():
    endpoint = "ref-data/symbols"
    data = stock_api(endpoint)
    if data['success']:
        data['data'] = [x for x in data['data'] if
                        x['type'] in ['cs', 'et'] and
                        x['isEnabled'] and
                        not x['symbol'] in bad_symbols]
    return data

def stock_batch(symbols=None, types='ohlc', range='1m'):
    endpoint = "stock/market/batch?{}types={}&range={}".format(('' if symbols == None else 'symbols=' + symbols + '&'),
                                                               types, range)
    data = stock_api(endpoint)
    return data

def stock_batch_100(types='ohlc', range='1m'):
    result = {}
    symbols = stock_symbols()
    if symbols['success']:
        result['data'] = {}
        lst_sym = []
        for sym in symbols['data']:
            lst_sym.append(sym['symbol'])
            if len(lst_sym) == 100:
                batch_100 = stock_batch(','.join(lst_sym), types, range)
                if batch_100['success']:
                    for k, v in batch_100['data'].items():
                        result['data'][k] = v
                lst_sym[:] = []
        if len(lst_sym) > 0:
            batch_100 = stock_batch(','.join(lst_sym), types, range)
            if batch_100['success']:
                for k, v in batch_100['data'].items():
                    result['data'][k] = v
        result['success'] = True
        result['error'] = None
    else:
        result['data'] = None
        result['success'] = False
        result['error'] = symbols['error']
    return result

def stock_book(symbol):
    endpoint = "stock/{}/book".format(symbol)
    data = stock_api(endpoint)
    return data

def stock_chart(symbol, range='1m'):
    endpoint = "stock/{}/chart/{}".format(symbol, range)
    data = stock_api(endpoint)
    return data

def stock_company(symbol):
    endpoint = "stock/{}/company".format(symbol)
    data = stock_api(endpoint)
    return data

def stock_delayed_quote(symbol):
    endpoint = "stock/{}/delayed-quote".format(symbol)
    data = stock_api(endpoint)
    return data

def stock_earnings(symbol):
    endpoint = "stock/{}/earnings".format(symbol)
    data = stock_api(endpoint)
    return data

def stock_effective_spread(symbol):
    endpoint = "stock/{}/effective-spread".format(symbol)
    data = stock_api(endpoint)
    return data

def stock_dividends(symbol, range='1m'):
    endpoint = "stock/{}/dividends/{}".format(symbol, range)
    data = stock_api(endpoint)
    return data

def stock_financials(symbol):
    endpoint = "stock/{}/financials".format(symbol)
    data = stock_api(endpoint)
    return data

def stock_stats(symbol):
    endpoint = "stock/{}/stats".format(symbol)
    data = stock_api(endpoint)
    return data

def stock_ohlc(symbol=None):
    endpoint = "stock/{}/ohlc".format(('market' if symbol == None else symbol))
    data = stock_api(endpoint)
    for key in (str(key) for key in range(4)):
        if key in data['data']:
            del data['data'][key]
    return data

def stock_peers(symbol):
    endpoint = "stock/{}/peers".format(symbol)
    data = stock_api(endpoint)
    return data

def stock_previous(symbol=None):
    endpoint = "stock/{}/previous".format(('market' if symbol == None else symbol))
    data = stock_api(endpoint)
    return data

def stock_price(symbol):
    endpoint = "stock/{}/price".format(symbol)
    data = stock_api(endpoint)
    return data

def stock_quote(symbol, displayPercent=False):
    endpoint = "stock/{}/quote{}".format(symbol, ('?displayPercent=true' if displayPercent else ''))
    data = stock_api(endpoint)
    return data

def stock_relevant(symbol):
    endpoint = "stock/{}/relevant".format(symbol)
    data = stock_api(endpoint)
    return data

def stock_splits(symbol, range='1m'):
    endpoint = "stock/{}/splits/{}".format(symbol, range)
    data = stock_api(endpoint)
    return data

def stock_volume_by_venue(symbol):
    endpoint = "stock/{}/volume-by-venue".format(symbol)
    data = stock_api(endpoint)
    return data

# -------------------------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 60)
    print('test iex_api.py...')
    print('-' * 60)
    stats = stock_stats('AAPL')
    if stats['success']:
        print('AAPL stats')
        for key in stats['data']:
            print('{} : {}'.format(key, stats['data'][key]))
    print('-' * 60)
